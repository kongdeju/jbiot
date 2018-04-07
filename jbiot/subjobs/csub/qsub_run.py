#!/usr/bin/env python
#coding=utf-8
import os
import subprocess
import time

def gen_qsub(cmdid,mem,cmd):
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
%s
        """ % (jobname,log,log,cmd)
    qsub =  cmdid + ".qsub"
    qsub = os.path.join(taskdir,qsub)
    fp = open(qsub,"w")
    fp.write(line)
    fp.close()
    return qsub,log

def check_qsub(jobid):
    cmd = "qstat -j %s" % jobid
    p = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    p.wait()
    stdinfo = p.stdout.read()
    steinfo = p.stderr.read()
    if stdinfo.find("error reason") != -1:
        return 2 
    if stdinfo:
        return 0
    if steinfo:
        return 1
    return   

def execute_qsub(qsubfile):
    cmd = "qsub %s" % qsubfile
    p = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    p.wait()
    stdinfo = p.stdout.read()
    steinfo = p.stderr.read()
    if  steinfo:
        return None
    jobid = stdinfo.split()[2]
    while True:
        status = check_qsub(jobid)
        if status:
            return jobid
        time.sleep(2)

def status_qsub(jobid):
    cmd = "qacct -j %s" % jobid
    p = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    p.wait()
    stdinfo = p.stdout.read()
    steinfo = p.stderr.read()
    code1 = 1
    code2 = 1
    for line in stdinfo.split("\n"):
        if line.startswith("exit_status"):
            code1 = int(line.split()[-1])
        if line.startswith("failed"):
            code2 = int(line.split()[-1])
    
    if code1 :
        return code1
    if code2:
        return code2
    
    return 0
    
def qsub_run(cmdid,cmdmem,cmd):
    qsubfile,logfile = gen_qsub(cmdid,cmdmem,cmd) 
    jobid = execute_qsub(qsubfile)
    status = status_qsub(jobid)
    return status,logfile,jobid


if __name__ == "__main__":
    import sys
    cmdid = sys.argv[1]
    cmdmem = sys.argv[2]
    cmd = sys.argv[3]
    status,logfile,jobid = qsub_run(cmdid,cmdmem,cmd)
    print status,logfile,jobid
