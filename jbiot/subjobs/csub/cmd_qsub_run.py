#!/usr/bin/env python
#coding=utf-8
import os
import subprocess
import time
import sys

def infocmd(cmd):
    sys.stderr.write(cmd + "\n")
    p = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    p.wait()
    info1 = p.stdout.read()
    info2 = p.stderr.read()
    info = info1  + "\n" + info2 + "\n"
    sys.stderr.write(info)

status_run = "/lustre/users/kongdeju/DevWork/jbiot/bin/status_run.py"
if not  os.path.exists(status_run):
    status_run = "status_run.py"

def cmd_adapt(cmdfile,mem,cpu):
    cmdid = cmdfile.split("/")[-1].split(".")[0]
    # clean old status
    statusfile = os.path.join(".status","%s.status" % cmdid)
    finishfile = os.path.join(".status","%s.finished" % cmdid)
    cmd = "rm -f %s 1>>/dev/null 2>>/dev/null" % statusfile
    os.system(cmd)
    cmd = "rm -f %s 1>>/dev/null 2>>/dev/null" % finishfile
    os.system(cmd)

    logdir = ".log"
    taskdir = ".task"
    if not os.path.exists(logdir):
        os.system("mkdir -p %s" % logdir)
    
    if not os.path.exists(taskdir):
        os.system("mkdir -p %s" % taskdir)
    
    log = os.path.join(logdir, cmdid + ".log")
    jobname = "task-%s" % cmdid
    line = """#!/bin/bash 
#$ -S /bin/bash
#$ -cwd
#$ -N %s
#$ -o %s
#$ -e %s
#$ -l h_vmem=%s,cpu=%s
%s %s
        """ % (jobname,log,log,mem,cpu,status_run,cmdid)
    qsub =  cmdid + ".qsub"
    qsub = os.path.join(taskdir,qsub)
    fp = open(qsub,"w")
    fp.write(line)
    fp.close()
    return qsub

def cmd_check(cmdfile):
    cid = cmdfile.split("/")[-1].split(".")[0]
    flag = os.path.join( ".status", "%s.finished" % cid )
    while True:
        if os.path.exists(flag):
            break
    time.sleep(5)

def cmd_run(qsubfile,cmdfile):
    cid = cmdfile.split("/")[-1].split(".")[0]
    cmd = "qsub %s" % qsubfile
    sys.stderr.write(cmd+"\n")
    p = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    p.wait()
    stdinfo = p.stdout.read()
    steinfo = p.stderr.read()
    sys.stderr.write(steinfo+"\n")
    sys.stderr.write(stdinfo+"\n")
    jobid = stdinfo.split()[2]
    cmd = "mkdir -p .jids/qsub"
    os.system(cmd)
    fp = open(".jids/qsub/%s"%cid,"w")
    fp.write("%s"%jobid)
    fp.close()
    return jobid

def cmd_status(cmdfile):
    status = 0
    cid = cmdfile.split("/")[-1].split(".")[0]
    logfile = os.path.join(".log",cid+".log")
    statusfile = os.path.join(".status",cid+".status")
    if os.path.exists(statusfile):
        status = 1
    return status,logfile

def main(cmdfile,mem,cpu):
    qsubfile = cmd_adapt(cmdfile,mem,cpu) 
    jobid = cmd_run(qsubfile,cmdfile)
    cmd_check(cmdfile)
    status,logfile = cmd_status(cmdfile)
    print status,logfile,jobid 


if __name__ == "__main__":

    from docopt import docopt

    usage = """
    Usage:
        cmd_qsub_run.py [options] <cmdfile> 

    Options:
        --cpu=<cpu>        cpu nums want to use [default: 4]
        --mem=<mem>        memory want to use [default: 8G]

    """
    args = docopt(usage)
    cpu = args["--cpu"]
    mem = args["--mem"]
    cmdfile = args["<cmdfile>"]
    main(cmdfile,cpu,mem)

