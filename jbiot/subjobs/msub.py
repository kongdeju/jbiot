#!/usr/bin/env python
#coding=utf-8
import re
import os
import subprocess
import time
import sys
from multiprocessing import Process

pat1 = re.compile("--mem[= ](\d+)")
def csub(stepfile):
    stepdir = ".steps" 
    if not os.path.exists(stepdir):
        os.mkdir(stepdir)
 
    mem = "2G" 
    fp = open(stepfile)
    
    cmds =  []
    for line in fp.readlines():
        line = line.strip()
        if not line :
            continue
        if line.startswith("#"):
            mat = pat1.search(line)
            if mat :
                mem = mat.group(1)
            continue
        cmds.append(line)
    prex = stepfile.split("/")[-1]

    qsubfiles = [] 
    for i in range(len(cmds)):
        qjob_ =  "qsub.%s.%02d" % (prex,i)
        qjob = os.path.join(stepdir,qjob_)
        qjob1 = qjob + ".stdout.log"
        qjob2 = qjob + ".stderr.log"
        cmd = cmds[i]
        line = """#!/bin/bash 
#$ -S /bin/bash
#$ -cwd
#$ -N %s
#$ -o %s
#$ -e %s
date
echo executing %s 
%s
date
echo finished
        """ % (qjob_,qjob1,qjob2,cmd,cmd)
        fp = open(qjob,"w")
        fp.write(line)
        fp.close()
        qsubfiles.append(qjob)
    return qsubfiles


def checkJob(jobid):
    cmd = "qstat -j %s" % jobid
    p = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    stdinfo = p.stdout.read()
    steinfo = p.stderr.read()
    if stdinfo:
        return 0
    if steinfo:
        return 1
    return   

def execute(qsubfile):
    
    cmd = "qsub %s" % qsubfile
    print "executing... %s " % cmd
    p = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    stdinfo = p.stdout.read()
    steinfo = p.stderr.read()
    if  steinfo:
        return

    jobid = stdinfo.split()[2]
    while True:
        status = checkJob(jobid)
        if status:
            return
        time.sleep(2)

    
def msub(step):
    steps = csub(step)
    ps = []
    for step in steps:
        p = Process(target=execute,args=(step,))
        p.start()
        ps.append(p)

    for p in ps:
        p.join()
    
    return 

if __name__ == "__main__":
    from docopt import docopt    
    usage = """
    Usage:
        csub.py <cmdfile> 

    Options:
        <cmdfile>      submit cmdfile to cluster run in parallize mod
    """ 
    args = docopt(usage)
    cmd = args["<cmdfile>"]
    msub(cmd)

 
