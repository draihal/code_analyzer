"""Parser for most common function name."""

import ast
import os
import collections

from nltk import pos_tag, download as download_nltk_data


class PathDoesNotExist(Exception):
    pass


class FuncNameParser:
    def __init__(self, path, projects=('',), top_size=10):
        if not os.path.exists(path):
            raise PathDoesNotExist()

        self.path = path
        self.projects = projects
        self.top_size = top_size
        self.words = []

        self.parse_func_name(self.top_size)


    def convert_list_of_tuple_to_list(self, list_of_tuple):
        """[(1,2), (3,4)] -> [1, 2, 3, 4]"""
        return [item for tuple_ in list_of_tuple for item in tuple_]


    def is_verb(self, word):
        if not word:
            return False
        try:
            pos_info = pos_tag([word])
            return pos_info[0][1] == 'VB'
        except LookupError:
            download_nltk_data('averaged_perceptron_tagger')
            pos_info = pos_tag([word])
            return pos_info[0][1] == 'VB'


    def get_trees(self, path, with_filenames=False, with_file_content=False):
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


    def get_verbs_from_function_name(self, function_name):
        return [word for word in function_name.split('_') if self.is_verb(word)]


    def get_top_verbs_in_path(self, path, top_size):
        trees = [t for t in self.get_trees(path) if t]
        fncs = [f for f in self.convert_list_of_tuple_to_list([[node.name.lower() for node in ast.walk(t) if isinstance(node, ast.FunctionDef)] for t in trees]) if not (f.startswith('__') and f.endswith('__'))]
        verbs = self.convert_list_of_tuple_to_list([self.get_verbs_from_function_name(function_name) for function_name in fncs])
        return collections.Counter(verbs).most_common(top_size)


    def get_all_names(tree):
        return [node.id for node in ast.walk(tree) if isinstance(node, ast.Name)]


    def get_all_words_in_path(path):
        trees = [t for t in get_trees(path) if t]
        function_names = [f for f in convert_list_of_tuple_to_list([get_all_names(t) for t in trees]) if not (f.startswith('__') and f.endswith('__'))]

        def split_snake_case_name_to_words(name):
            return [n for n in name.split('_') if n]

        return convert_list_of_tuple_to_list([split_snake_case_name_to_words(function_name) for function_name in function_names])


    def get_top_functions_names_in_path(path, top_size=10):
        t = get_trees(path)
        nms = [f for f in convert_list_of_tuple_to_list([[node.name.lower() for node in ast.walk(t) if isinstance(node, ast.FunctionDef)] for t in t]) if not (f.startswith('__') and f.endswith('__'))]
        return collections.Counter(nms).most_common(top_size)


    def parse_func_name(self, top_size):
        for project in self.projects:
            path = os.path.join(self.path, project)
            self.words += self.get_top_verbs_in_path(path, top_size)
        c = collections.Counter()
        for word, count in self.words:
            c[word] += count
        if len(c) == 0:
            result = 'There is no function name.'
        elif len(c) < top_size:
            result = f'All function name: {list(c.items())}'
        else:
            result = f'Top {top_size} function name: {list(c.items())[0:top_size]}'
        print(result)
