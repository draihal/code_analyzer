import argparse
import os
from pathlib import Path

from .args_validators import ValidateGitURL, ValidatePositiveInt, ValidateOSPath
# from ..setup import DESCRIPTION, VERSION, NAME
# sys.path.append(sys.path[0] + "/..")
# ValueError: attempted relative import beyond top-level package

NAME = 'code_analyzer'
DESCRIPTION = 'Get most common words from code.'
VERSION = '0.0.2'


def create_parser():
    """Make parser class."""
    parser = argparse.ArgumentParser(
        prog=NAME,
        description=DESCRIPTION,
        add_help=False
    )
    parser.add_argument(
        '-p', '--path', type=Path,
        default=Path(os.getcwd()), action=ValidateOSPath,
        help='Path to the directory with code to analyse, default current directory',)
    parser.add_argument(
        '-g', '--github_path',
        default=None, action=ValidateGitURL,
        help='The URL to github repository with code to analyse, default None',)
    parser.add_argument(
        '-l', '--lookup', type=str,
        default='v', choices=['v', 'w', 'a'],
        help='''Type of analyzing, default "v". 
            "v" - ..., 
            "a" - ...,
            "w" - ...''',)
    parser.add_argument(
        '-pr', '--projects', type=set,
        default=('',),
        help='Dirnames with projects with code to analyse, default current directory',)
    parser.add_argument(
        '-s', '--top_size', type=int,
        default=10, action=ValidatePositiveInt,
        help='Top amount of words to report, default 10',)
    parser.add_argument(
        '-n', '--number_filenames', type=int,
        default=100, action=ValidatePositiveInt,
        help='Max numbers of filenames to analyse, default 100',)
    parser.add_argument(
        '-o', '--output_format',
        default=None, choices=['json', 'txt', 'csv'],
        help='Output report file format to current directory, default output to cli',)

    parser.add_argument(
        '-h', '--help',
        action='help', help='Help',)
    parser.add_argument(
        '-v', '--version',
        action='version',
        help='Version',
        version='%(prog)s {}'.format('VERSION'),)
    return parser
