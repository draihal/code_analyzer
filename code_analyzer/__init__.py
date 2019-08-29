#!/usr/bin/python
# -*- coding: UTF-8 -*-

import sys
# import itertools
# import threading
# import time

from .core import CodeAnalyzer
from .output import make_output
from .parse_args import create_parser


def main():
    """Entry point for the application script."""
    parser = create_parser()
    namespace = parser.parse_args(sys.argv[1:])

    # done = False
    #
    # # here is the animation
    # def animate():
    #     for c in itertools.cycle(['|', '/', '-', '\\']):
    #         if done:
    #             break
    #         sys.stdout.write('\rAnalyzing ' + c)
    #         sys.stdout.flush()
    #         time.sleep(0.1)
    #
    # t = threading.Thread(target=animate)
    # t.start()
    #
    # # long process here
    # time.sleep(10)

    report = CodeAnalyzer(
        path=namespace.path,
        lookup=namespace.lookup,
        projects=namespace.projects,
        top_size=namespace.top_size,
        len_filenames=namespace.number_filenames,
        github_path=namespace.github_path,
    ).parse()
    # done = True
    make_output(namespace.output_format, report)
    sys.stdout.write('\rDone!')
