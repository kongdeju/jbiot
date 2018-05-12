import os
import yaml
import hashlib
import sys
from multiprocessing import Pool
import subprocess
from ..jblog import jblog
from ..stopjobs import lstop
import time
import re
import signal
cmdstatus = ".status"
pat = re.compile(r"(docker|singularity)[\s\S]+\$PWD\s+(.+?)\s+(.+)")
import os

parent_id = os.getpid()
pid_pat =  re.compile("\((\d+?)\)")
def init_worker():
    def sig_init2(signal_num,frame):
        lstop()
        cmd = "pstree -p %s" % parent_id
        p = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        out = p.stdout.read()
        pids = pid_pat.findall(out)
        pids = set(pids)
        for pid in pids:
            pid = int(pid)
            cmd = "kill -9 %s 1>>/dev/null 2>>/dev/null" % pid
            os.system(cmd)
        
        cmd = "kill -9 %s 1>>/dev/null 2>>/dev/null" % parent_id
        os.system(cmd)

        cmd = "kill -9 %s 1>>/dev/null 2>>/dev/null" % os.getpid()
        os.system(cmd)
        sys.exit()
    signal.signal(signal.SIGINT, sig_init2)

def checkstatus(cid):
    if not os.path.exists(cmdstatus):
        os.mkdir(cmdstatus)
    s = os.path.join(cmdstatus,cid+".status")
    if os.path.exists(s):
        return 1
    return 0


cmd_run = "/lustre/users/kongdeju/DevWork/jbiot/jbiot/subjobs/lsub/cmd_lsub_run.py"
if not os.path.exists(cmd_run):
    cmd_run = "cmd_lsub_run.py"

def run(cmdfile,rerun=False,verbose=False):
    cid = cmdfile.split("/")[-1].split(".")[0]
    cmd = open(cmdfile).read().strip("\n")
    icmd= cmd
    mat = pat.search(cmd)
    if mat :
        icmd = mat.groups()[-1]

    info = """    exec... %s""" % icmd
    if verbose:
        info = """    exec... %s
        %s """ % ( cmd,os.path.join(".log",cid+".log"))
    jblog(info)

    s = 0
    status = "\033[1;33mfailed\033[0m"
    if rerun:
        s = checkstatus(cid)
    if s:
        status = "\033[1;32mpassed\033[0m"
    logdir = ".log"
    d = "mkdir -p %s" % logdir
    os.system(d)
    logfile = os.path.join(logdir,cid+".log")
    fp = open(logfile,"w")
    lcmd = "%s %s" % (cmd_run,cmdfile)
    fp.write(lcmd+"\n\n")
    fp.close()
    if not s:
        p = subprocess.Popen(lcmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        p.wait()
        stdinfo = p.stdout.read()
        steinfo = p.stderr.read()
        if stdinfo :
            s,logfile,jobid = stdinfo.strip().split()
            s = int(s)
            if s:
                s = 1
                status = "\033[1;32msuccess\033[0m"
            else:
                s = 0
                status = "\033[1;33mfailed\033[0m"
        fp = open(logfile,"a")
        fp.write(steinfo)
        fp.close()

    info = """
    finish... %s
        status: %s
        logfile: %s
    """ % (icmd,status,logfile)
    if verbose:
        logcmd = "cat %s" % logfile
        p = subprocess.Popen(logcmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        p.wait()
        log = p.stdout.read()
        info = """
    finish... %s
        status: %s
        logfile: %s
        details: %s
        """ % (cmd,status,logfile,log)
    jblog(info)
    return s

def parsecmd(cmdfile,rerun,debug):
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
        cmdf = os.path.join(taskdir,cid + ".cmd")
        fp = open(cmdf,"w")
        line = cmd + "\n"
        fp.write(line)
        fp.close()
        torun.append(cmdf)
    return torun


def main(cmdfile,threads,rerun,debug):
    jblog("\nexecuting %s ...\n" % cmdfile)
    cmdfiles = parsecmd(cmdfile,rerun,debug)
    maxline = len(cmdfiles)
    if threads> maxline: threads = maxline
    pools = Pool(threads,initializer=init_worker)
    fail = 1
    try:
        ps = []
        for cmdfile in cmdfiles:
            p = pools.apply_async(run,(cmdfile,rerun,debug)) 
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
        sys.exit()

    return fail

if __name__ == "__main__":
    from docopt import docopt
    usage = """
    Usage:
        lsub_run.py <cmdfile> [-j <threads> ] 

    Options:
        cmdfile                  cmd in shell format.
        -j,--threads=<threads>   num of threads.

    """
    args = docopt(usage)
    cmdfile = args["<cmdfile>"]
    threads = args["--threads"]
    main(cmdfile,threads)
