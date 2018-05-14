#!/usr/bin/env python
#coding=utf-8
import sys
import os
dirpath = os.path.join(os.path.dirname(os.path.abspath(__file__)),"../")
sys.path.insert(0,dirpath)
from jbiot.subjobs.csub.cmd_qsub_run import main



if __name__ == "__main__":

    from docopt import docopt

    usage = """
    Usage:
        cmd_qsub_run.py [options] <cmdfile>

    Options:
        --cpu=<cpu>        cpu nums want to use [default: 1]
        --mem=<mem>        memory want to use [default: 2G]

    """
    args = docopt(usage)
    cpu = args["--cpu"]
    mem = args["--mem"]
    cmdfile = args["<cmdfile>"]
    main(cmdfile,cpu,mem)

