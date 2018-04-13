#!/usr/bin/env python
#coding=utf-8
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
import os
dirpath = os.path.join(os.path.dirname(os.path.abspath(__file__)),"../")
sys.path.insert(0,dirpath)
from jbiot.subjobs.status_run import status_run



if __name__ == "__main__":
    from docopt import docopt

    Usage = """
    Usage:
        status_run.py [options] <cmd>

    Description:
        run cmdfile with sh. and return codefile in .status dicectory.

    Options:
        cmd             cmd file in bash format
        -w,--dir=dir    oss working directory  

    """
    args = docopt(Usage)
    cmd = args["<cmd>"]
    wdir = args["--dir"]
    status_run(cmd,wdir)
