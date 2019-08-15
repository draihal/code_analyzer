"""Parser for most common function name."""

import ast
import collections
import os

from nltk import download as download_nltk_data, pos_tag


class FuncNameParser:
    def __init__(self, path, lookup='v', projects=('',), top_size=10):
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
        self.words = []

    def _convert_tpls_to_lst(self, list_of_tuple):
        """[(1,2), (3,4)] -> [1, 2, 3, 4]"""
        return [item for tuple_ in list_of_tuple for item in tuple_]

    def _is_verb(self, word):
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
        filenames = []
        trees = []
        for dirname, dirs, files in os.walk(path, topdown=True):
            for file in files:
                if file.endswith('.py'):
                    filenames.append(os.path.join(dirname, file))
                    if len(filenames) == 100:
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
        return [word for word in function_name.split('_')
                if self._is_verb(word)]

    def _is_dunder(self, name):
        """ __name__ """
        return name.startswith("__") and name.endswith("__")

    def _get_all_names(self, tree):
        return [node.id for node in ast.walk(tree)
                if isinstance(node, ast.Name)]

    def _get_all_func_names(self, tree):
        return [node.name.lower() for node in ast.walk(tree)
                if isinstance(node, ast.FunctionDef)]

    def _get_converted_names(self, trees, func):
        return [f for f in self._convert_tpls_to_lst([func(t) for t in trees])
                if not self._is_dunder(f)]

    def _get_count_most_common(self, list_words, top_size):
        return collections.Counter(list_words).most_common(top_size)

    def _get_top_verbs_in_path(self, path, top_size):
        trees = self._get_trees(path)
        fncs = self._get_converted_names(trees, self._get_all_func_names)
        verbs = self._convert_tpls_to_lst(
            [self._get_verbs_from_function_name(function_name)
                for function_name in fncs])
        return self._get_count_most_common(verbs, top_size)

    def _get_all_words_in_path(self, path, top_size):
        trees = self._get_trees(path)
        function_names = self._get_converted_names(trees, self._get_all_names)
        all_words_in_path = self._convert_tpls_to_lst(
            [[n for n in function_name.split('_') if n]
                for function_name in function_names])
        return self._get_count_most_common(all_words_in_path, top_size)

    def _get_top_functions_names_in_path(self, path, top_size):
        trees = self._get_trees(path)
        fncs = self._get_converted_names(trees, self._get_all_func_names)
        return self._get_count_most_common(fncs, top_size)

    def parse(self):
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
