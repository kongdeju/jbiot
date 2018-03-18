#!/usr/bin/env python
#coding=utf-8
from threading import Thread
import os
import time
import sys
dirpath = os.path.join(os.path.dirname(os.path.abspath(__file__)),"../")
sys.path.insert(0,dirpath)
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

def always(cmd,timeout):
    startime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    jd.add([pid,startime,cmd])
    
    while True:
        trd = Thread(target=runcmd,args=(cmd,))
        trd.start()
        trd.join(timeout)
        if trd.is_alive():
            trd._Thread__stop()


if __name__ == "__main__":
    import sys
    from docopt import docopt
    usage = """
    Usage:
        alwaysrun.py <cmd> [-t <timeout> ] 
    
    Options:
        <cmd>                   cmd to run
        -t,--timeout=timeout    timeout(seconds) to rerun for next run[default: 259200]
    """
    args = docopt(usage)
    cmd = args["<cmd>"]
    timeout = args["--timeout"]
    if not timeout.isdigit(): print  usage
    timeout = int(timeout)
    always(cmd,timeout)

