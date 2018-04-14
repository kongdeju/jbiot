import sys
import os
import subprocess

def status_run(cmdfile,wdir):
    cid = cmdfile.split("/")[-1].split(".")[0]
    logdir = ".log"
    cmd = "mkdir -p %s" % logdir
    os.system(cmd)
    logfile = os.path.join(logdir,cid+".log")

    cmd = "sh %s " % cmdfile
    fp = open(logfile,"w")
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
    statusfile = os.path.join(cmdstatus,cid+".status") 
    os.system("rm -rf %s 1>>/dev/null 2>>/dev/null" % cmdstatus)
    code = sum(codes)
    print code    
    if not code:
        cmd = "mkdir -p %s" % cmdstatus
        os.system(cmd)
        os.system("touch %s" % (statusfile))

    if wdir:
        statdir = os.path.join(wdir,".status/")
        cmd = "oss2tools.py upload %s %s" % (statusfile,statdir)
        os.system(cmd)
        logdir = os.path.join(wdir,".log/")
        cmd = "oss2tools.py upload %s %s" % (logfile,logdir) 
        os.system(cmd)
