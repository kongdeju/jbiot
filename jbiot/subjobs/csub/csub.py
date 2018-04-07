#!/usr/bin/env python
from csub_strip import stripcmd
import csub_run 
import os
import sys

def csub(cmd,dry,rerun,verbose,force):
    tasks = stripcmd(cmd)
    if dry:
        return
    for task in tasks:
        cmdfile = task[0]
        mem = task[1]
        fail = csub_run.main(cmdfile,mem,rerun,verbose)
        if fail:
            print "\033[1;31m"
            print "contain failure,job stopped..."
            print "\033[0m"
            if not force:
                sys.exit(1)
            print "go execute cause force mode is set on..."
