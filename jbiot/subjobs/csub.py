#!/usr/bin/env python
from cmdStep import cmdStep
from msub import msub

import os

def csub(cmd):
    
    cmdfiles = cmdStep(cmd)
    cmdparas = []
    for cmdfile in cmdfiles:
        msub(cmdfile)
      

if __name__ == "__main__":
    
    from docopt import docopt

    usage = """
    Usage:
        csub.py <cmdfile>

    Options:
        -h --help        print this screen
    """
    args = docopt(usage) 
    cmdfile = args["<cmdfile>"]
    csub(cmdfile)

   

    
    

