#!/usr/bin/env python
#coding=utf-8
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
import os
dirpath = os.path.join(os.path.dirname(os.path.abspath(__file__)),"../")
sys.path.insert(0,dirpath)

from jbiot.subjobs.cmd2showdoc import cmd2showdoc



if __name__ == "__main__":
    from docopt import docopt
    usage = """
    
    Usage:
        cmd2showdoc.py <cmdfile> -t <title> 

    Intro:
        cmd2showdoc.py is designed to upload cmdfile to showdoc server.

    Options:
        <cmdfile>                      cmdfile in markdown format
        -t,--title=<title>             title of page on showdoc

    """
    args = docopt(usage)
    cmd = args["<cmdfile>"]
    title = args["--title"]
    cmd2showdoc(title,cmd)

