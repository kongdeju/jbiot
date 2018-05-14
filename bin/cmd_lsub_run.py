#!/usr/bin/env python
#coding=utf-8
import sys
import os
dirpath = os.path.join(os.path.dirname(os.path.abspath(__file__)),"../")
sys.path.insert(0,dirpath)
from jbiot.subjobs.lsub.cmd_lsub_run import main


if __name__ == "__main__":
    from docopt import docopt

    usage="""
    Usage:
        cmd_lsub_run.py  <cmdfile>

    """
    args = docopt(usage)

    cmdfile = args["<cmdfile>"]
    main(cmdfile)

