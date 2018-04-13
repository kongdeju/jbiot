#!/usr/bin/env python
#coding=utf-8
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
import os
dirpath = os.path.join(os.path.dirname(os.path.abspath(__file__)),"../")
sys.path.insert(0,dirpath)
from jbiot.subjobs.csub.qsub_run import qsub_run

if __name__ == "__main__":
    import sys
    cmdfile = sys.argv[1]
    cmdid = cmdfile.split("/")[-1].split(".")[0]
    fp = open(cmdfile)
    cmdmem = fp.readline()
    cmdmem = cmdmem.strip("\n")
    cmd = fp.readline()
    cmd = cmd.strip("\n")
    fp.close()
    status,logfile,jobid = qsub_run(cmdid,cmdmem,cmd)
    print status,logfile,jobid

