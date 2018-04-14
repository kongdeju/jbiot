#!/usr/bin/env python
#coding=utf-8
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
import os
dirpath = os.path.join(os.path.dirname(os.path.abspath(__file__)),"../")
sys.path.insert(0,dirpath)
from jbiot.subjobs.alisub.cmd_bc_run import cmd_run

if __name__ == "__main__":
    from docopt import docopt

    usage = """
    Usage:
        cmd_bc_run.py [options] <cmdfile> 

    Options:
        --wdir=<widr>      oss working directory
        --cpu=<cpu>        cpu nums want to use [default: 1]
        --mem=<mem>        memory want to use [default: 2G]
        --docker=<docker>  docker images wants to use [default: jbioi/alpine-dev]

    """
    args = docopt(usage)
    wdir = args["--wdir"]
    cpu = args["--cpu"]
    mem = args["--mem"]
    docker = args["--docker"]
    cmdfile = args["<cmdfile>"]
    cmdid = cmdfile.split("/")[-1].split(".")[0]
    cmd = open(cmdfile).readline().strip()
    cmd_run(cmdid,cmd,wdir,cpu,mem,docker)

