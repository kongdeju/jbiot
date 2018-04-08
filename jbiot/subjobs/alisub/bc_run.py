#!/usr/bin/env python
#coding=utf-8
import os
import subprocess
import time

def gen_bc(cmdid,mem,cmd):
    pass
def finish_bc(jobid):
    pass
def execute_bc(qsubfile):
    pass
def status_qsub(jobid):
    pass 
def bc_run(cmdid,cmdmem,cmd):
    pass

if __name__ == "__main__":
    import sys
    cmdid = sys.argv[1]
    cmdmem = sys.argv[2]
    cmd = sys.argv[3]
    status,logfile,jobid = qsub_run(cmdid,cmdmem,cmd)
    print status,logfile,jobid
