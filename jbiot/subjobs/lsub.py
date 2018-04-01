#!/usr/bin/env python
from lsub_strip import stripcmd
import lsub_run 
from dockersing import dockersing
import os
import sys

def lsub(cmd,dry,rerun,verbose,force):
    tasks = stripcmd(cmd)
    if dry:
        return
    for task in tasks:
        cmdfile = task[0]
        para = task[1]
        fail = lsub_run.main(cmdfile,para,rerun,verbose)
        if fail:
            print "\033[1;31m"
            print "contain failure,job stopped..."
            print "\033[0m"
            if not force:
                sys.exit(1)
            print "go execute cause force mode is set on..."

def main(cmd,dryflag,docker=False,sing=False,rerun=False,verbose=False,force=False):
    if docker:
        cmd = dockersing(cmd,prefer="docker")
    if sing:
        cmd = dockersing(cmd,prefer="singularity")
    cmdrun = lsub(cmd,dryflag,rerun,verbose,force)
    return cmd
