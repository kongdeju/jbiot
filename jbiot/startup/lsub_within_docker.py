#!/usr/bin/env python
import os

def lsub_with_docker(args=[]):
    
    args = " ".join(args) 
    cmd = "docker run -v $PWD:$PWD -w $PWD --rm kongdeju/alpine-dev:stable lsub.py %s" % args
    os.system(cmd)

if __name__ == "__main__":
    import sys
    args = sys.argv[1:]
    lsub_with_docker(args)


