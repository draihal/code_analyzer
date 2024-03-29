import logging
import os
import shutil
import tempfile

from git import Repo

from .ast_analysis import _get_all_names, _get_all_func_names, _generate_trees
from .ntlk_analysis import _get_verbs_from_function_name, _get_nouns_from_function_name
from .utils import _get_count_most_common, _get_converted_names, _convert_tpls_to_lst

logging.basicConfig(
    filename='code_analyzer.log',
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%d-%b-%y %H:%M:%S',
    level=logging.INFO)


class CodeAnalyzer:
    """Code analyzer main class."""

    def __init__(
            self,
            path='C:\\',
            lookup='verb',
            projects=('', ),
            top_size=10,
            len_filenames=100,
            github_path=None,
    ):
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
        trees = (_generate_trees(filename, with_filenames,
                                 with_file_content)[0]
                 for filename in filenames)
        logging.info("Trees generated.")
        return trees

    def _get_top_verbs_in_path(self, path):
        """
        Returns a list of tuples with words and his counts.
        :param path: path
        :return: list of tuples with words and his counts
        """
        trees = self._get_trees(path)
        fncs = _get_converted_names(trees, _get_all_func_names)
        verbs = (_get_verbs_from_function_name(function_name)
                 for function_name in fncs)
        converted_verbs = _convert_tpls_to_lst(verbs)
        return converted_verbs

    def _get_top_nouns_in_path(self, path):
        """
        Returns a list of tuples with words and his counts.
        :param path: path
        :return: list of tuples with words and his counts
        """
        trees = self._get_trees(path)
        fncs = _get_converted_names(trees, _get_all_func_names)
        nouns = (_get_nouns_from_function_name(function_name)
                 for function_name in fncs)
        converted_nouns = _convert_tpls_to_lst(nouns)
        return converted_nouns

    def _get_all_words_in_path(self, path):
        """
        Returns a list of tuples with words and his counts.
        :param path: path
        :return: list of tuples with words and his counts
        """
        trees = self._get_trees(path)
        function_names = _get_converted_names(trees, _get_all_names)
        all_words_in_path = ((word for word in function_name.split('_')
                              if word) for function_name in function_names)
        converted_all_words_in_path = _convert_tpls_to_lst(all_words_in_path)
        return converted_all_words_in_path

    def _get_top_functions_names_in_path(self, path):
        """
        Returns a list of tuples with words and his counts.
        :param path: path
        :return: list of tuples with words and his counts
        """
        trees = self._get_trees(path)
        fncs = _get_converted_names(trees, _get_all_func_names)
        return fncs

    def _parse_lookup_args(self, path_):
        """
        Parse arguments for lookup.
        :param path_: path
        :return: None
        """
        # verb - show statistics of the most common words by verbs
        # noun - show statistics on the most frequent words by nouns
        # funcname - show statistics of the most common words function names
        # localvarname - show statistics of the most common
        #                words names of local variables inside functions
        lookups_functions = {
            'verb': self._get_top_verbs_in_path,
            'noun': self._get_top_nouns_in_path,
            'funcname': self._get_top_functions_names_in_path,
            'localvarname': self._get_all_words_in_path,
        }
        for project in self.projects:
            path = os.path.join(path_, project)
            function_for_lookup = lookups_functions.get(self.lookup)
            self.words += function_for_lookup(path)

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
            top_words = _get_count_most_common(self.words, self.top_size)
            try:
                shutil.rmtree(tmpdir)
            except PermissionError:
                logging.info(
                    'Can\'t deleting temp directory.  Access is denied.')
            logging.info('Done!')
            return [] if len(top_words) == 0 else top_words
        else:
            self._parse_lookup_args(self.path)
            top_words = _get_count_most_common(self.words, self.top_size)
            logging.info("Done!")
            return [] if len(top_words) == 0 else top_words
