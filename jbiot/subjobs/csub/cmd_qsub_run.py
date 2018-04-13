#!/usr/bin/env python
#coding=utf-8
import os
import subprocess
import time
import sys

def getscript(script):
    p = subprocess.Popen('which %s' % script ,shell=True,stdout=subprocess.PIPE)
    p.wait()
    info = p.stdout.read()
    info = info.strip()
    if info:
        qsub_run = script
    else:
        qsub_run = "/lustre/users/kongdeju/DevWork/jbiot/bin/status_run.py"
    return qsub_run

status_run = getscript("status_run.py")

def gen_qsub(cmdfile,mem,cpu):
    cmdid = cmdfile.split("/")[-1].split(".")[0]
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
%s %s
        """ % (jobname,log,log,status_run,cmdfile)
    qsub =  cmdid + ".qsub"
    qsub = os.path.join(taskdir,qsub)
    fp = open(qsub,"w")
    fp.write(line)
    fp.close()
    return qsub

def check_qsub(jobid):
    cmd = "qstat -j %s" % jobid
    p = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    p.wait()
    stdinfo = p.stdout.read()
    steinfo = p.stderr.read()
    if stdinfo.find("error reason") != -1:
        return 1 
    if steinfo:
        return 1
    return   

def execute_qsub(qsubfile):
    cmd = "qsub %s" % qsubfile
    sys.stderr.write(cmd+"\n")
    p = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    p.wait()
    stdinfo = p.stdout.read()
    steinfo = p.stderr.read()
    sys.stderr.write(steinfo+"\n")
    sys.stderr.write(stdinfo+"\n")
    jobid = stdinfo.split()[2]
    while True:
        status = check_qsub(jobid)
        if status:
            return jobid
        time.sleep(5)

def status_qsub(cmdfile):
    status = 0
    cid = cmdfile.split("/")[-1].split(".")[0]
    logfile = os.path.join(".log",cid+".log")
    statusfile = os.path.join(".status",cid+".status")
    if os.path.exists(statusfile):
        status = 1
    return status,logfile

def qsub_run(cmdfile,mem,cpu):
    qsubfile = gen_qsub(cmdfile,mem,cpu) 
    jobid = execute_qsub(qsubfile)
    status,logfile = status_qsub(cmdfile)
    print status,logfile,jobid 
    return status,logfile,jobid


if __name__ == "__main__":

    from docopt import docopt

    usage = """
    Usage:
        cmd_qsub_run.py [options] <cmdfile> 

    Options:
        --cpu=<cpu>        cpu nums want to use [default: 1]
        --mem=<mem>        memory want to use [default: 2G]

    """
    args = docopt(usage)
    cpu = args["--cpu"]
    mem = args["--mem"]
    cmdfile = args["<cmdfile>"]
    qsub_run(cmd,cpu,mem)
