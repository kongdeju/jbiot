import os
import yaml
import hashlib
import sys
from multiprocessing import Pool,Process
import subprocess
qsub_run = os.path.join(os.path.dirname(os.path.abspath(__file__)),"qsub_run.py")

cmdstatus = ".status"
def checkstatus(cid):
    if not os.path.exists(cmdstatus):
        os.mkdir(cmdstatus)
    s = os.path.join(cmdstatus,cid)
    if os.path.exists(s):
        return 1

def addstatus(cid):
    if not os.path.exists(cmdstatus):
        os.mkdir(cmdstatus)
    cp = os.path.join(cmdstatus,cid)
    cmd = "touch %s" % cp
    os.system(cmd)

def run(cid,cmd,cmdmem,rerun=False,verbose=False):
    s = 0
    status = "\033[1;33mfailed\033[0m"
    if rerun:
        s = checkstatus(cid)
    if s:
        status = "\033[1;32mpassed\033[0m"
    logfile = os.path.join(".log","%s.log"%cid)
    qcmd = "%s %s %s '%s'" % (qsub_run,cid,cmdmem,cmd)
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
                status = "\033[1;33mfailed\33[0m"
            else:
                s = 1
                status = "\033[1;32msuccess\33[0m"
                addstatus(cid)

    info = """
    exec... %s
        status: %s
        logfile:%s
        """ % (cmd,status,logfile)

    if verbose:
        logcmd = "cat %s" % logfile
        p = subprocess.Popen(logcmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        p.wait()
        log = p.stdout.read()
        qsubfile = os.path.join(".task",cid+".qsub")
        info = """
    exec... %s
        status: %s
        qsubfile: %s
        logfile: %s
        details: %s
        """ % (cmd,status,qsubfile,logfile,log)
    print info
    return s

def parsecmd(cmdfile,cmdmem,rerun,debug):
    fp = open(cmdfile)
    ct = cmdfile
    torun = []
    for line in fp.readlines():
        ct = ct + line
        cid = hashlib.md5(ct)
        cid = cid.hexdigest()
        cmd = line.strip()
        torun.append([cid,cmd,cmdmem,rerun,debug])
    return torun

def main(cmdfile,cmdmem,rerun,debug):
    print "\nexecuting %s ..." % cmdfile
    torun = parsecmd(cmdfile,cmdmem,rerun,debug)
    pools = Pool(len(torun))
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
    print "%s failed,%s success" % (fail,suc)
    
    return fail

