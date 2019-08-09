import unittest
from func_name_parser.core import FuncNameParser


class FuncNameParserTestCase(unittest.TestCase):

    def setUp(self):
        self.path = 'C:\\'
        self.path_does_not_exist = 'CCC:\\'
        self.lokup = 'test'
        self.projects = (
            'testproject1',
            'testproject2',
        )


    def test_path_that_does_not_exist(self):
        self.assertRaises(
            Exception,
            FuncNameParser,
            self.path_does_not_exist,
        )

    def test_lokup_that_does_not_exist(self):
        self.assertRaises(
            Exception,
            FuncNameParser,
            self.path,
            self.lokup,
        )
