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
        md2html.py <md> [ -s <style> ] 
    
    md2html.py is designed to transfer markdown file to html file 
    using mkdocs to build this process.

    Options:
       -h --help            just print this screen
       <md>                 markdown format file
       -s,--style=<style>    
       output               default ouput html.tgz
    """
    args = docopt(usage)
    md = args["<md>"]
    style = args["--style"]
    md2html(md,style)

