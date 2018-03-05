#!/usr/bin/env python

import sys
import os
dirpath = os.path.join(os.path.dirname(os.path.abspath(__file__)),"../")
sys.path.insert(0,dirpath)
from jbiot import csub
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

