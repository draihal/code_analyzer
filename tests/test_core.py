import unittest
from func_name_parser.core import FuncNameParser, PathDoesNotExist


class FuncNameParserTestCase(unittest.TestCase):

    def setUp(self):
        self.path = 'C:\\'
        self.path_does_not_exist = 'CCC:\\'
        self.projects = (
            'testproject1',
            'testproject2',
        )


    def test_pass_path_that_does_not_exist(self):
        self.assertRaises(
            PathDoesNotExist,
            FuncNameParser,
            self.path_does_not_exist
        )
