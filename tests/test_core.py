import unittest
from code_analyzer import CodeAnalyzer


class FuncNameParserTestCase(unittest.TestCase):

    def setUp(self):
        self.path = 'C:\\'
        self.path_does_not_exist = 'CCC:\\'
        self.lookup = 'test'
        self.projects = (
            'testproject1',
            'testproject2',
        )
        self.wrong_top_size = 0
        self.len_filenames = 0

    def test_path_that_does_not_exist(self):
        self.assertRaises(
            Exception,
            CodeAnalyzer,
            self.path_does_not_exist,
        )

    def test_lokup_that_does_not_exist(self):
        self.assertRaises(
            Exception,
            CodeAnalyzer,
            self.path,
            lookup=self.lookup,
        )

    def test_wrong_top_size(self):
        self.assertRaises(
            Exception,
            CodeAnalyzer,
            self.path,
            top_size=self.wrong_top_size,
        )

    def test_wrong_len_filenames(self):
        self.assertRaises(
            Exception,
            CodeAnalyzer,
            self.path,
            len_filenames=self.len_filenames,
        )
