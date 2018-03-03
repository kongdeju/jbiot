#!/usr/bin/env python
from cmdStep import cmdStep
from msub import msub

import os
from dockersing import dockersing

def csub(cmd,docker,sing):
    if docker:
        cmd = dockersing(cmd,prefer="docker")
    if sing:
        cmd = dockersing(cmd,prefier="singularity")      
    
    cmdfiles = cmdStep(cmd)
    cmdparas = []
    for cmdfile in cmdfiles:
        msub(cmdfile)
      

if __name__ == "__main__":
    
    from docopt import docopt

    usage = """
    Usage:
        csub.py <cmdfile> [--with-docker|--with-singularity]

    Options:
        -h --help           print this screen
        --with-docker       prefer to user docker when exec cmd
        --with-singularity  prefer to user singularity when exec cmd
    """
    args = docopt(usage) 
    cmdfile = args["<cmdfile>"]
    docker = args["--with-docker"]
    sing = args["--with-singularity"]
    csub(cmdfile,docker=docker,sing=sing)

   

    
    

