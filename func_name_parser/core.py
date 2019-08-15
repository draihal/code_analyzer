"""Parser for most common function name."""

import ast
import collections
import os

from nltk import download as download_nltk_data, pos_tag


class FuncNameParser:
    def __init__(
        self, path, lookup='v',
        projects=('',), top_size=10,
        len_filenames=100
        ):
        if not os.path.exists(path):
            raise Exception(
                'Something wend wrong. Is your path correct?\n'
                f'It should be like: "C\\py\\". Your path is: "{path}".\n'
            )
        if lookup not in ['a', 'v', 'w']:
            raise Exception(
                'Something wend wrong. Is your lookup correct?\n'
                f'It should be: "a", "v" or "w". Your lookup is: "{lookup}".\n'
            )
        if top_size <= 0:
            raise Exception(
                'Something wend wrong. Is your top size correct?\n'
                f'It should be > 0. Your top size is {top_size}.\n'
            )

        self.path = path
        self.lookup = lookup
        self.projects = projects
        self.top_size = top_size
        self.len_filenames = len_filenames
        self.words = []

    def _convert_tpls_to_lst(self, list_of_tuple):
        """
        Convert list of tuples to list.
        [(1,2), (3,4)] -> [1, 2, 3, 4]
        :param list_of_tuple: list of tuple
        :return: list
        """
        return [item for tuple_ in list_of_tuple for item in tuple_]

    def _is_verb(self, word):
        """
        Returns the boolean value of whether the word is a verb.
        :param word: word
        :return: boolean - True or False
        """
        if not word:
            return False
        try:
            pos_info = pos_tag([word])
            return pos_info[0][1] == 'VB'
        except LookupError:
            download_nltk_data('averaged_perceptron_tagger')
            pos_info = pos_tag([word])
            return pos_info[0][1] == 'VB'

    def _get_trees(self, path, with_filenames=False, with_file_content=False):
        """
        Returns lists of ast objects.
        :param path: path
        :return: lists of ast objects
        """
        filenames = []
        trees = []
        for dirname, dirs, files in os.walk(path, topdown=True):
            for file in files:
                if file.endswith('.py'):
                    filenames.append(os.path.join(dirname, file))
                    if len(filenames) == self.len_filenames:
                        break
        for filename in filenames:
            with open(filename, 'r', encoding='utf-8') as attempt_handler:
                main_file_content = attempt_handler.read()
            try:
                tree = ast.parse(main_file_content)
            except SyntaxError as e:
                print(e)
                tree = None
            if with_filenames:
                if with_file_content:
                    trees.append((filename, main_file_content, tree))
                else:
                    trees.append((filename, tree))
            else:
                trees.append(tree)
        return trees

    def _get_verbs_from_function_name(self, function_name):
        """
        Returns list with verb.
        :param function_name: function name
        :return: lists with verb
        """
        return [word for word in function_name.split('_')
                if self._is_verb(word)]

    def _is_dunder(self, name):
        """
        Returns boolean is a name a dunder method.
        Like this: __name__.
        :param name: name
        :return: boolean - True or False
        """
        return name.startswith("__") and name.endswith("__")

    def _get_all_names(self, tree):
        """
        Returns list of all words.
        :param tree: _ast.Module object
        :return: list with words
        """
        return [node.id for node in ast.walk(tree)
                if isinstance(node, ast.Name)]

    def _get_all_func_names(self, tree):
        """
        Returns list of all words.
        :param tree: _ast.Module object
        :return: list with words
        """
        return [node.name.lower() for node in ast.walk(tree)
                if isinstance(node, ast.FunctionDef)]

    def _get_converted_names(self, trees, func):
        """
        Returns a list of words.
        :param trees: list of _ast.Module object
        :param func: function
        :return: list with words
        """
        return [word for word in self._convert_tpls_to_lst(
                [func(tree) for tree in trees])
                if not self._is_dunder(word)]

    def _get_count_most_common(self, list_words, top_size):
        """
        Returns a list of tuples with words and his counts.
        :param list_words: list of words
        :param top_size: number of top words
        :return: list of tuples with words and his counts
        """
        return collections.Counter(list_words).most_common(top_size)

    def _get_top_verbs_in_path(self, path, top_size):
        """
        Returns a list of tuples with words and his counts.
        :param path: path
        :param top_size: number of top words
        :return: list of tuples with words and his counts
        """
        trees = self._get_trees(path)
        fncs = self._get_converted_names(trees, self._get_all_func_names)
        verbs = self._convert_tpls_to_lst(
            [self._get_verbs_from_function_name(function_name)
                for function_name in fncs])
        return self._get_count_most_common(verbs, top_size)

    def _get_all_words_in_path(self, path, top_size):
        """
        Returns a list of tuples with words and his counts.
        :param path: path
        :param top_size: number of top words
        :return: list of tuples with words and his counts
        """
        trees = self._get_trees(path)
        function_names = self._get_converted_names(trees, self._get_all_names)
        all_words_in_path = self._convert_tpls_to_lst(
            [[word for word in function_name.split('_') if word]
                for function_name in function_names])
        return self._get_count_most_common(all_words_in_path, top_size)

    def _get_top_functions_names_in_path(self, path, top_size):
        """
        Returns a list of tuples with words and his counts.
        :param path: path
        :param top_size: number of top words
        :return: list of tuples with words and his counts
        """
        trees = self._get_trees(path)
        fncs = self._get_converted_names(trees, self._get_all_func_names)
        return self._get_count_most_common(fncs, top_size)

    def parse(self):  #TODO: logging
        """
        Returns a list of tuples with words and his counts.

        :return: list of tuples with words and his counts
        """
        for project in self.projects:
            path = os.path.join(self.path, project)
            if self.lookup == 'v':
                self.words += self._get_top_verbs_in_path(path, self.top_size)
            elif self.lookup == 'a':
                self.words += self._get_all_words_in_path(path, self.top_size)
            elif self.lookup == 'w':
                self.words += self._get_top_functions_names_in_path(
                    path, self.top_size)
        count_words = collections.Counter()
        for word, count in self.words:
            count_words[word] += count
        return 0 if len(count_words) == 0 else [(word, count)
                    for word, count in count_words.items()]
