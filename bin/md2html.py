#!/usr/bin/env python

import sys
import os
dirpath = os.path.join(os.path.dirname(os.path.abspath(__file__)),"../")
sys.path.insert(0,dirpath)

from jbiot.md2html import md2html


if __name__ == "__main__":

    from docopt import docopt

    usage = """
    Usage:
        md2html.py <md>

    Options:
       -h --help     just print this screen
       mdfile        markdown format file
       output        default is html directory. and also html.tgz
    """
    args = docopt(usage)

    md = args["<md>"]
    md2html(md)

