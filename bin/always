#!/usr/bin/env python
#coding=utf-8
from threading import Thread
import os
import time
import sys

dirpath = os.path.join(os.path.dirname(os.path.abspath(__file__)),"../")
sys.path.insert(0,dirpath)
alwaysrun = os.path.join(os.path.dirname(os.path.abspath(__file__)),"alwaysrun.py")

from jbiot.jsondb import jsondb
home = os.environ["HOME"]
tgtdir = os.path.join(home,".always")
if not os.path.exists(tgtdir):
    os.mkdir(tgtdir)

db = os.path.join(tgtdir,"always.json")
jd = jsondb(db)
pid = os.getpid()

def runcmd(cmd):
    print cmd
    os.system(cmd)    

def listall():
    adict = jd.getall()
    head = "alwaysID\tStarTime\tCMD" 
    print head
    print 
    for k,v in adict.items():
        line = "%s\t%s\t%s" % (k,v[1],v[2])
        print line

def stopjob(aid):
    pid = jd.get(aid)[0]
    cmd = "kill -9 %s" % pid
    os.system(cmd)
    jd.remove(aid)

def always(cmd,timeout,deamon):

    CMD = "%s '%s' -t %s" % (alwaysrun,cmd,timeout)
    if deamon: 
        CMD = "nohup %s '%s' -t %s 1>>run.log 2>>run.log &" % (alwaysrun,cmd,timeout)
    print CMD
    os.system(CMD)
    
    
if __name__ == "__main__":
    import sys
    from docopt import docopt
    usage = """
    Usage:
        always run <cmd> [-t <timeout> ][-d] 
        always list
        always stop <aid>
    
    Overview:
        always is used to run soft in deamain mode with timeout time to rerun

    Options:
        <cmd>                   cmd to run
        -t,--timeout=timeout    timeout(seconds) to rerun for next run[default: 259200]
        -d,--deamon             deamon mode    
    """
    args = docopt(usage)
    run = args["run"]
    lst = args["list"]
    stop = args["stop"]
    aid = args["<aid>"]
    cmd = args["<cmd>"]
    timeout = args["--timeout"]
    deamon = args["--deamon"]
    if not timeout.isdigit(): print  usage
    timeout = int(timeout)
    if run:
        always(cmd,timeout,deamon)
    if lst:
        listall()
    if stop:
        stopjob(aid)

