import sys
import os
import subprocess

def status_run(cid,wdir):

    logdir = ".log"
    cmd = "mkdir -p %s" % logdir
    os.system(cmd)
    logfile = os.path.join(logdir,cid+".log")
    cmdfile = os.path.join(".task","%s.cmd"%cid)

    if wdir :
        taskdir = os.path.join(wdir,".task")
        cmd = "oss2tools.py download %s ." % (taskdir)
        os.system(cmd)
        print cmd
        cmdfile = os.path.join(".task","%s.bc.cmd"%cid)
 
    fp = open(logfile,"a")
    codes = []
    fp2 = open(cmdfile)
    for line in fp2.readlines():
        cmd = line.strip()
        p = subprocess.Popen(cmd,shell=True,stdout=fp,stderr=fp)
        code = p.wait()
        codes.append(code)
        if code:
            print "Error:",cmd
            break

    cmdstatus = ".status"
    cmd = "mkdir -p %s" % cmdstatus
    os.system("mkdir -p %s" % cmdstatus)

    finishfile = os.path.join(cmdstatus,cid+".finished")
    os.system("rm -f %s 1>>/dev/null 2>>/dev/null" % finishfile)
    statusfile = os.path.join(cmdstatus,cid+".status") 
    os.system("rm -f %s 1>>/dev/null 2>>/dev/null" % statusfile)
    code = sum(codes)

    os.system("touch %s" % finishfile)
    if not code:
        os.system("touch %s" % (statusfile))

    if wdir:
        statdir = os.path.join(wdir,".status/")
        cmd = "oss2tools.py upload %s %s" % (statusfile,statdir)
        os.system(cmd)
        logdir = os.path.join(wdir,".log/")
        cmd = "oss2tools.py upload %s %s" % (logfile,logdir) 
        os.system(cmd)
