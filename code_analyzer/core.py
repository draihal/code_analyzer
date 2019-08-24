import collections
import logging
import os
import shutil
import tempfile

from git import Repo

from .ast_analysis import _get_all_names, _get_all_func_names, _generate_trees
from .ntlk_analysis import _get_verbs_from_function_name
from .utils import _convert_tpls_to_lst, _get_count_most_common, _get_converted_names


logging.basicConfig(
    filename='code_analyzer.log',
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%d-%b-%y %H:%M:%S',
    level=logging.INFO)


class CodeAnalyzer:
    """Code analyzer main class."""
    def __init__(
            self, path='C:\\', lookup='v',
            projects=('',), top_size=10,
            len_filenames=100, github_path=None,):
        logging.info("Program started.")
        self.path = path
        self.github_path = github_path
        self.lookup = lookup
        self.projects = projects
        self.top_size = top_size
        self.len_filenames = len_filenames
        self.words = []

    def _get_filenames(self, path):
        """
        Get filenames from path.
        :param path: path
        :return: list
        """
        filenames = []
        for dirname, dirs, files in os.walk(path, topdown=True):
            for file in files:
                if file.endswith('.py'):
                    filenames.append(os.path.join(dirname, file))
                    if len(filenames) == self.len_filenames:
                        break
        logging.info(f"Path is: {path}.")
        logging.info(f"Total {len(filenames)} files.")
        return filenames

    def _get_trees(self, path, with_filenames=False, with_file_content=False):
        """
        Returns lists of ast objects.
        :param path: path
        :return: lists of ast objects
        """
        filenames = self._get_filenames(path)
        trees = [_generate_trees(filename, with_filenames, with_file_content)[0]
                 for filename in filenames]
        logging.info("Trees generated.")
        return trees

    def _get_top_verbs_in_path(self, path, top_size):
        """
        Returns a list of tuples with words and his counts.
        :param path: path
        :param top_size: number of top words
        :return: list of tuples with words and his counts
        """
        trees = self._get_trees(path)
        fncs = _get_converted_names(trees, _get_all_func_names)
        verbs = _convert_tpls_to_lst(
            [_get_verbs_from_function_name(function_name)
                for function_name in fncs])
        return _get_count_most_common(verbs, top_size)

    def _get_all_words_in_path(self, path, top_size):
        """
        Returns a list of tuples with words and his counts.
        :param path: path
        :param top_size: number of top words
        :return: list of tuples with words and his counts
        """
        trees = self._get_trees(path)
        function_names = _get_converted_names(trees, _get_all_names)
        all_words_in_path = _convert_tpls_to_lst(
            [[word for word in function_name.split('_') if word]
                for function_name in function_names])
        return _get_count_most_common(all_words_in_path, top_size)

    def _get_top_functions_names_in_path(self, path, top_size):
        """
        Returns a list of tuples with words and his counts.
        :param path: path
        :param top_size: number of top words
        :return: list of tuples with words and his counts
        """
        trees = self._get_trees(path)
        fncs = _get_converted_names(trees, _get_all_func_names)
        return _get_count_most_common(fncs, top_size)

    def _parse_lookup_args(self, path_):
        """
        Parse arguments for lookup.
        :param path_: path
        :return: None
        """
        for project in self.projects:
            path = os.path.join(path_, project)
            if self.lookup == 'v':
                self.words += self._get_top_verbs_in_path(path, self.top_size)
            # if self.lookup == 'n':
            #     self.words += self._get_top_nouns_in_path(path, self.top_size)
            elif self.lookup == 'a':
                self.words += self._get_all_words_in_path(path, self.top_size)
            elif self.lookup == 'w':
                self.words += self._get_top_functions_names_in_path(
                    path, self.top_size)

    def parse(self):
        """
        Returns a list of tuples with words and his counts.
        :return: list of tuples with words and his counts
        """
        if self.github_path:
            tmpdir = tempfile.mkdtemp()
            logging.info(f'Created temporary directory: {tmpdir}.')
            Repo.clone_from(self.github_path, tmpdir)
            self._parse_lookup_args(tmpdir)
            count_words = collections.Counter()
            for word, count in self.words:
                count_words[word] += count
            try:
                shutil.rmtree(tmpdir)
            except PermissionError:
                logging.info('Can\'t deleting temp directory.  Access is denied.')
            logging.info('Done!')
            return 0 if len(count_words) == 0 else [(word, count)
                                                    for word, count in count_words.items()]
        else:
            self._parse_lookup_args(self.path)
            count_words = collections.Counter()
            for word, count in self.words:
                count_words[word] += count
            logging.info("Done!")
            return 0 if len(count_words) == 0 else [(word, count)
                        for word, count in count_words.items()]
