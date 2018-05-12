#!/usr/bin/env python
import os
import subprocess
import time

status_run = "/lustre/users/kongdeju/DevWork/jbiot/bin/status_run.py"
if not  os.path.exists(status_run):
    status_run = "status_run.py"

def cmd_status(cmdfile):
    cid = cmdfile.split("/")[-1].split(".")[0]
    flag = os.path.join(".status",cid+".status")
    logfile = os.path.join(".log",cid+".log")
    status = 0
    if os.path.exists(flag):
        status = 1
    return status,logfile        


def cmd_check(cmdfile):
    cid = cmdfile.split("/")[-1].split(".")[0]
    flag = os.path.join( ".status", "%s.finished" % cid )
    while True:
        if os.path.exists(flag):
            break
        time.sleep(5)

def cmd_run(cmdfile):

    cid = cmdfile.split("/")[-1].split(".")[0]

    # clean old status
    statusfile = os.path.join(".status","%s.status" % cid)
    finishfile = os.path.join(".status","%s.finished" % cid)
    cmd = "rm -f %s 1>>/dev/null 2>>/dev/null" % statusfile
    os.system(cmd)
    cmd = "rm -f %s 1>>/dev/null 2>>/dev/null" % finishfile
    os.system(cmd)

    cmd = "nohup %s %s 1>>/dev/null 2>>/dev/null &" % (status_run,cid)
    p = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,preexec_fn=os.setpgrp)
    pid = str(p.pid)
    cmd = "mkdir -p .jids/local"
    os.system(cmd)

    ppid = os.getpid()
    fp = open(".jids/local/%s"%cid,"w")
    fp.write("%s\t%s"%(pid,ppid))
    fp.close()
    return pid

def main(cmdfile):
    jobid = cmd_run(cmdfile)
    cmd_check(cmdfile)
    status,logfile = cmd_status(cmdfile)
    print status,logfile,jobid

if __name__ == "__main__":
    from docopt import docopt
    
    usage="""
    Usage:
        cmd_lsub_run.py  <cmdfile>

    """
    args = docopt(usage)

    cmdfile = args["<cmdfile>"]
    main(cmdfile)
