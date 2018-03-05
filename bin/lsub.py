#!/usr/bin/env python

import sys
import os
dirpath = os.path.join(os.path.dirname(os.path.abspath(__file__)),"../")
sys.path.insert(0,dirpath)
from jbiot import lsub

if __name__ == "__main__":

    from docopt import docopt

    usage = """
    Usage:
        lsub.py <cmdfile>  [--dry] [--with-docker|--with-singularity]

    Options:
        -h --help           print this screen
        --dry               all done but run script
        --with-docker       prefer to use docker when run cmd
        --with-singularity  prefer to user singularity when run cmd

    """
    args = docopt(usage)
    cmdfile = args["<cmdfile>"]
    dryflag = args["--dry"]
    docker = args["--with-docker"]
    sing = args["--with-singularity"]
    lsub.main(cmdfile,dryflag,docker=docker,sing=sing)
 




