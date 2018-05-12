import os
import signal
import glob
import sys
import re
import subprocess
import time

pid_pat =  re.compile("\((\d+?)\)")
pid = os.getpid()
cwd = os.getcwd()
def lstop():
    lj = os.path.join(cwd,".jids/local")
    idfiles = glob.glob("%s/*" % lj )
    for idf in idfiles:
        pid,ppid = open(idf).read().strip().split("\t")
        pid = int(pid)
        ppid = int(ppid)
        try:
            os.killpg(pid,signal.SIGTERM)  
            os.kill(ppid,signal.SIGTERM)  
        except:
            pass
        os.system("rm %s 1>>/dev/null 2>>/dev/null " % idf)

def Lstop(parent_id):

    if 1:
        cmd = "pstree -p %s" % parent_id
        p = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        out = p.stdout.read()
        pids = pid_pat.findall(out)
        pids = set(pids)
        if not pids:
            print "children is empty"
        for pid in pids:
            pid = int(pid)
            if pid == parent_id:
                continue
            try:
                os.kill(pid,signal.SIGKILL)
            except Exception,e:
                print e
        os.kill(parent_id,signal.SIGKILL)    

def cstop():
    lj = os.path.join(cwd,".jids/qsub")
    idfiles = glob.glob("%s/*" % lj )
    for idf in idfiles:
        pid = open(idf).read().strip()
        cmd = "qdel %s" % pid
        os.system(cmd)
        os.system("rm %s 1>>/dev/null 2>>/dev/null" % idf)

def alistop():
    lj = os.path.join(cwd,".jids/bcs")
    idfiles = glob.glob("%s/*" % lj )
    for idf in idfiles:
        pid = open(idf).read().strip()
        cmd = "bcs sj %s" % pid
        os.system(cmd)
        os.system("rm %s 1>>/dev/null 2>>/dev/null " % idf)

def stopdeamon():
    dea = os.path.join(cwd,".jids","deamon.pid")
    if os.path.exists(dea):
        pid = int(open(dea).read().strip())
        try:
            os.killpg(pid,signal.SIGTERM)
        except Exception , e:
            print e
        os.system("rm %s 1>>/dev/null 2>>/dev/null " % dea)

def stopmain():
    dea = os.path.join(cwd,".jids","main.pid")
    if os.path.exists(dea):
        pid = int(open(dea).read().strip())
        try:
            os.kill(pid,signal.SIGTERM)
        except Exception ,e :
            print e
        os.system("rm %s 1>>/dev/null 2>>/dev/null " % dea)

def stopjobs():
    print "stop jobs..."
    lstop()
    stopmain()
    stopdeamon()
    cstop()
    alistop()
    sys.exit()

if __name__ == "__main__":
    stopjobs()

