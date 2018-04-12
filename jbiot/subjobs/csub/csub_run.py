import os
import yaml
import hashlib
import sys
from multiprocessing import Pool,Process
import subprocess
qsub_run = os.path.join(os.path.dirname(os.path.abspath(__file__)),"qsub_run.py")
from ..jblog import jblog
import signal
import time
import psutil

cmdstatus = ".status"
def checkstatus(cid):
    if not os.path.exists(cmdstatus):
        os.mkdir(cmdstatus)
    s = os.path.join(cmdstatus,cid)
    if os.path.exists(s):
        return 1
    return 0

def addstatus(cid):
    if not os.path.exists(cmdstatus):
        os.mkdir(cmdstatus)
    cp = os.path.join(cmdstatus,cid)
    cmd = "touch %s" % cp
    os.system(cmd)

def run(cid,cmd,cmdfile,rerun=False,verbose=False):
    info = """    exec... %s""" % cmd
    jblog(info)

    s = 0
    status = "\033[1;33mfailed\033[0m"
    cid = cmdfile.split("/")[-1].split(".")[0]
    if rerun:
        s = checkstatus(cid)
    if s:
        status = "\033[1;32mpassed\033[0m"
    logfile = os.path.join(".log","%s.log"%cid)
    qcmd = '%s %s ' % (qsub_run,cmdfile)
    fp = open(logfile,"w")
    fp.write(qcmd+"\n")
    fp.close()
    jobid = None
    if not s:
        p = subprocess.Popen(qcmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        p.wait()
        stdinfo = p.stdout.read()
        steinfo = p.stderr.read()
        if stdinfo:
            s,logfile,jobid = stdinfo.strip().split()
            s = int(s)
            if s:
                s = 0
                status = "\033[1;33mfailed\033[0m"
            else:
                s = 1
                status = "\033[1;32msuccess\033[0m"
                addstatus(cid)
        fp = open(logfile,"a")
        fp.write(steinfo)
        fp.close()

    info = """
    finish... %s
        status: %s
        jobid : %s
        logfile:%s
        """ % (cmd,status,jobid,logfile)

    if verbose:
        logcmd = "cat %s" % logfile
        p = subprocess.Popen(logcmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        p.wait()
        log = p.stdout.read()
        qsubfile = os.path.join(".task",cid+".qsub")
        info = """
    finish... %s
        status: %s
        qsubfile: %s
        jobid : %s
        logfile: %s
        details: %s
        """ % (cmd,status,qsubfile,jobid,logfile,log)
    jblog(info)
    return s

def parsecmd(cmdfile,cmdmem,rerun,debug):
    fp = open(cmdfile)
    ct = cmdfile
    torun = []
    taskdir = ".task"
    if not os.path.exists(taskdir):
        os.system("mkdir -p %s" % taskdir)
    for line in fp.readlines():
        ct = ct + line
        cid = hashlib.md5(ct)
        cid = cid.hexdigest()
        cmd = line.strip()
        cmdf = cid + ".cmd"
        cmdf = os.path.join(taskdir,cmdf)
        fp = open(cmdf,"w") 
        line = cmdmem + "\n"
        fp.write(line)
        line = cmd + "\n"
        fp.write(line)
        fp.close()
        torun.append([cid,cmd,cmdf,rerun,debug])
    return torun

parent_id = os.getpid()
def init_worker():
    def sig_int(signal_num, frame):
        parent = psutil.Process(parent_id)
        for child in parent.children():
            if child.pid != os.getpid():
                child.kill()
        parent.kill()
        psutil.Process(os.getpid()).kill()
    signal.signal(signal.SIGINT, sig_int)


def main(cmdfile,cmdmem,rerun,debug):
    jblog("\nexecuting %s ...\n" % cmdfile)
    torun = parsecmd(cmdfile,cmdmem,rerun,debug)
    pools = Pool(len(torun),init_worker)
    fail = 1
    try:
        ps = []
        for item in torun:
            p = pools.apply_async(run,item) 
            ps.append(p)
        pools.close()
        pools.join()
        outs = []
        for p in ps:
            s = p.get()
            outs.append(s)
        suc = outs.count(1)
        fail = outs.count(0)
        jblog("%s failed,%s success" % (fail,suc))
    except KeyboardInterrupt :
        print "Stop job..."
        pools.terminate()
        pools.join()

    return fail

