#!/usr/bin/env python
#coding=utf-8
import os
import subprocess
import time
import re
from ossio.oss2tools import osslist
import sys

def infocmd(cmd):

    sys.stderr.write(cmd + "\n")
    p = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    p.wait()
    info1 = p.stdout.read()
    info2 = p.stderr.read()
    info = info1  + "\n" + info2 + "\n"
    sys.stderr.write(info)


def handlecmdio(cmd):
    todowns = []
    toups   = []
    cmds = cmd.split(";")
    ncmds = []
    for cmd in cmds:
        cmd = cmd.strip()
        if cmd.startswith("I="):
            it = cmd[2:]
            if it == "null":
                continue
            its = it.split(",")
            todowns.extend(its)
        elif cmd.startswith("O="):
            it = cmd[2:]
            if it == "null":
                continue
            its = it.split(",")
            toups.extend(its)
        else:
            ncmds.append(cmd)
    ncmds = ";".join(ncmds) 
    return todowns,toups,ncmds

def checklocalandoss(fp,wdir,af):
    if af.startswith("/") or af.startswith("../") or af.startswith("~"):
        af = os.path.abspath(af)
        buc = wdir[6:].split("/")[0]
        datapath = os.path.join(buc,"data")
        datapath = "oss://" + datapath
        datapath = datapath + af
        objs = osslist(datapath,"")
        if objs:
            af = datapath
        else:
            if os.path.exists(af):
                cmd = "oss2tools.py upload %s %s" % (af,datapath)
                line = cmd + "\n"
                fp.write(line)
                af = datapath
    # relpath 
    else:
        datapath = os.path.join(wdir,af) 
        objs = osslist(datapath,"")
        if objs:
            pass
        else:
            if os.path.exists(af):
                cmd = "oss2tools.py upload %s %s" % (af,wdir)
                line = cmd + "\n"
                fp.write(line)
    return af 

def gen_lc(cid,wdir,cmd):
    if not wdir:
        wdir="oss://jbiobio/working/tmp"

    ins,outs,cmd = handlecmdio(cmd)
    tdir = ".task"
    if not os.path.exists(tdir):
        cmd = "mkdir -p %s" % tdir
        os.system(cmd)
    cmdfile = os.path.join(tdir,cid+".local.cmd")
    fp = open(cmdfile,"w")
    cmditems = re.split(r' +',cmd)
    if not ins:
        for i in range(len(cmditems)):
            cit = cmditems[i]
            if cit.startswith("-"):
                continue
            if cit.startswith("'"):
                continue
            if cit.startswith('"'):
                continue
            if cit.startswith("oss://"):
                continue
            nit =  checklocalandoss(fp,wdir,cit)
            cmditems[i] = nit
    else:
        for it in ins:
            if it.startswith("oss://"):
                continue
            else:
                nit = checklocalandoss(fp,wdir,it)
                cmditems[i] = nit
    fp.close()
    cmd = " ".join(cmditems)
    return cmdfile,cmd

#gen_lc("abc","oss://jbiobio/working/",'bwa mem -t 4 -R "RG\\tiullid" /tmp/reference oss://jbiobio/fq1 fq2')
#gen_lc("abc","oss://jbiobio/working/",'bwa mem -t 4 -R "RG\\tiullid" /tmp/reference oss://jbiobio/fq1 fq2')
#gen_lc("abc","oss://jbiobio/working/",'tar xvzf worker.tar.gz')

def execute_lc(cmdfile):
    cmd = "sh %s" % cmdfile
    infocmd(cmd)

def handle_input(fp,wdir,cmd):
    mcmd = "oss2tools.py mapdown %s" % wdir
    line = mcmd + "\n"
    fp.write(line)
    ins,outs,cmd = handlecmdio(cmd)

    #format cmd
    cmditems = re.split(r' +',cmd)
    osses = []
    cmds = []
    for cit in cmditems:
        if cit.startswith("oss://"):
            osses.append(cit)
            cit = cit[6:]
            cit = os.path.join("/tmp",cit)
        cmds.append(cit)
    ccmd = " ".join(cmds) 
   

    if not ins:
        # hanle abs oss
        for absoss in osses:
            cmd = "oss2tools.py absdown %s" % absoss
            line = cmd + "\n" 
            fp.write(line)            
        # hanle rel oss
        for cit in cmditems:
            if cit.startswith("-"):
                continue
            if cit.startswith("'"):
                continue
            if cit.startswith('"'):
                continue
            if cit.startswith("oss://"):
                continue
            cmd = "oss2tools.py reldown %s %s" % (wdir,cit)
            line = cmd + "\n"
            fp.write(line)
    else:
        for it in ins:
            if it.startswith("oss://"):
                cmd = "oss2tools.py absdown %s" % it
                line = cmd + "\n"
                fp.write(line)
            else:
                cmd = "oss2tools.py reldown %s %s" % (wdir,it)
                line = cmd + "\n"
                fp.write(line)
    # cmd ...
    line = ccmd + "\n"
    fp.write(line)

def handle_output(fp,wdir,cmd):
    ins,outs,cmd = handlecmdio(cmd)
    if outs:
        for it in outs:
            cmd = "oss2tools.py relup %s %s" % (wdir,it)
            cmd = cmd + "\n"
            fp.write(cmd)
    else:
        cmd = "oss2tools.py mapup %s" % wdir
        line = cmd + "\n"
        fp.write(cmd)

def gen_bc(cmdid,execcmd,wdir="oss://jbiobio/working/tmp"):
    tdir = ".task"
    if not os.path.exists(tdir):
        os.system("mkdir -p %s" % tdir)    
    cmdfile = cmdid + ".bc.cmd" 
    cmdfile = os.path.join(tdir,cmdfile)
    fp = open(cmdfile,"w")
    ftime = time.strftime('%Y-%m-%d-%H-%M-%S',time.localtime(time.time()))
    # ossdirmapping
    if not wdir:
        wdir = "oss://jbiobio/working/tmp/%s" % ftime

    # handle inputs
    handle_input(fp,wdir,execcmd)

    # hanle ouputs
    handle_output(fp,wdir,execcmd)

    fp.close()
    return cmdfile

#gen_bc("abc",'bwa mem -t 4 -R "RG\\tiullid" reference oss://jbiobio/fq1 fq2')
#gen_bc("abc",'bwa mem -t 4 -R "RG\\tiullid" reference oss://jbiobio/fq1 fq2;I=oss://bio/tmp/hg19.fq,fai;O=test.bam')

def finish_bc(jobid):
    
    status = 1
    cmd = "bcs check %s" % jobid
    p = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    p.wait()
    info = p.stdout.read()
    lines = info.split("\n")
    for line in lines:
        if line.startswith("JobName"):
            stat = line.split()[-1]
            if stat == "(Waiting)" or stat == "(Running)":
                status = 0
    return status

def execute_bc(cmdfile,docker="jbioi/alpine-dev",cpu=1,mem="2G"):
    
    img = "img-ubuntu"
    tp = "ecs.se1.xlarge"
   
    jobname = cmdfile.split("/")[-1].split(".")[0]
    timeout = 21600
    vpc = "192.168.0.0/16"
    jobid = None
    dockerstr = ""
    if docker:
        cmd = "docker pull docker.io/%s" % docker
        info = infocmd(cmd)
        cmd = "docker tag %s localhost:8864/%s" % (docker,docker)
        info = infocmd(cmd)
        cmd = "docker push localhost:8864/%s" % docker
        info = infocmd(cmd)
        dockerstr = " --docker=%s@oss://jbiobio/dockers/ " % docker
    cmd = "bcs sub 'sh %s' %s -i %s -t %s --vpc_cidr_block %s %s --disk system:default:500 --timeout=%s -p %s  -e PATH:/opt/conda/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin "  % (cmdfile.split("/")[-1],jobname,img,tp,vpc,dockerstr,timeout,cmdfile)
    sys.stderr.write(cmd+"\n")
    p = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    p.wait()
    info = p.stdout.read()
    steinfo = p.stderr.read()
    sys.stderr.write(info+"\n")
    sys.stderr.write(steinfo+"\n")
    lines = info.split("\n") 
    for line in lines:
        if line.startswith("Job created"):
            jobid = line.split(":")[-1].strip()
    return jobid

#execute_bc(".task/abc.cmd")

def status_bc(cid,jobid):
    status = 0
    cmd = "bcs job %s"
    p = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    p.wait()
    info = p.stdout.read()
    lines = info.split("\n")
    for line in lines:
        if line.startswith("| Id"):
            stat = line.strip("\n").strip("|").split("|")[-1].strip().split(":")[-1]
            if stat == "Finished":
                status = 1

    ldir = ".log"
    if not os.path.exists(ldir):
        os.system("mkdir -p %s" % ldir)
    logfile = cid + ".log"
    logfile = os.path.join(ldir,logfile)
    cmd = "bcs log %s" % jobid
    time.sleep(2)
    infocmd(cmd)
    #fp = open(logfile,"a")
    #p = subprocess.Popen(cmd,shell=True,stdout=fp,stderr=fp)
    #p.wait()
    #fp.close()

    return status,logfile

#status_bc("a","job-000000005ABA113000003043008F25EE")

def cmd_run(cmdid,cmd,cpu,mem,docker=None,wdir=None):
    localcmdfile,cmd = gen_lc(cmdid,wdir,cmd)
    bccmdfile = gen_bc(cmdid,cmd,wdir)
    execute_lc(localcmdfile)
    jobid = execute_bc(bccmdfile,docker,cpu,mem)
    while True:
        finish = finish_bc(jobid)
        if finish:
            break
        time.sleep(10)
    status,logfile = status_bc(cmdid,jobid)
    print status,logfile,jobid
    return status,logfile,jobid
if __name__ == "__main__":
    from docopt import docopt
    
    usage = """
    Usage:
        cmd_bc_run.py [options] <cmdfile> 

    Options:
        --cpu=<cpu>        cpu nums want to use [default: 1]
        --mem=<mem>        memory want to use [default: 2G]
        --docker=<docker>  docker images wants to use [default: jbioi/alpine-dev]

    """
    args = docopt(usage)
    cpu = args["--cpu"]
    mem = args["--mem"]
    docker = args["--docker"]
    cmdfile = args["<cmdfile>"]
    cmdid = cmdfile.split("/")[-1].split(".")[0]
    cmd = open(cmdfile).readline().strip()
    cmd_run(cmdid,cmd,cpu,mem,docker)
