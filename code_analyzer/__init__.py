#!/usr/bin/python
# -*- coding: UTF-8 -*-

import argparse
import sys
import os
from pathlib import Path
# sys.path.append(sys.path[0] + "/..")

from .core import CodeAnalyzer
# from ..setup import AUTHOR, DESCRIPTION, VERSION, NAME
# ValueError: attempted relative import beyond top-level package

NAME = 'code_analyzer'
DESCRIPTION = 'Get most common words from your code.'
AUTHOR = 'draihal'
VERSION = '0.0.2'


def create_parser():
    """Make parser class."""
    parser = argparse.ArgumentParser(
        prog=NAME,
        description=DESCRIPTION,
        epilog=f'''(c) {AUTHOR} 2019.''',
        add_help=False
    )

    parser.add_argument(
        '-p', '--path', type=Path,
        default=Path(os.getcwd()),
        help="Path to the code directory",)
    parser.add_argument(
        '-l', '--lookup', type=str,
        default='v', choices=['v', 'w', 'a'],
        help="Type of report")
    parser.add_argument(
        '-pr', '--projects', type=set,
        default=('',),
        help="Tuple with projects dir")
    parser.add_argument(
        '-s', '--top_size', type=int,
        default=10,
        help="")
    parser.add_argument(
        '-lf', '--len_filenames', type=int,
        default=100,
        help="")

    parser.add_argument('--help', '-h', action='help', help='Help')

    parser.add_argument('--version',
                        action='version',
                        help='Version',
                        version='%(prog)s {}'.format('VERSION'))
    return parser


def main():
    """Entry point for the application script"""
    parser = create_parser()
    namespace = parser.parse_args(sys.argv[1:])
    # print(namespace)
    print("Start analyse...\n")
    report = CodeAnalyzer(
        namespace.path,
        namespace.lookup,
        namespace.projects,
        namespace.top_size,
        namespace.len_filenames,
    ).parse()
    print("Your result is: ", report)

