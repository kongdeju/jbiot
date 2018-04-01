import os
import yaml
import hashlib
import sys
from multiprocessing import Pool
import subprocess

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

def run(cid,cmd,rerun=False,verbose=False):
    s = 0
    if rerun:
        s = checkstatus(cid)
    if s:
        status = "passed"
    logdir = ".log"
    d = "mkdir -p %s" % logdir
    os.system(d)
    logfile = os.path.join(logdir,cid)
    fp = open(logfile,"w")
    if not s:
        p = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        flag = p.wait()
        stdinfo = p.stdout.read() + "\n"
        errinfo = p.stderr.read() + "\n"
        fp.write("standard output1:\n")
        fp.write(stdinfo)
        fp.write("standard output2:\n")
        fp.write(errinfo)
        fp.close()
        if verbose:
            os.system("cat %s" % logfile)
        if flag == 0 :
            status = "success"
            addstatus(cid)
            s = 1
        else:
            s = 0
            status = "failed check detail \033[1;31m %s \033[0m" % logfile
    print "\t%s   %s" % (cmd,status)
    return s

def parsecmd(cmdfile,rerun,debug):
    fp = open(cmdfile)
    ct = cmdfile
    torun = []
    for line in fp.readlines():
        ct = ct + line
        cid = hashlib.md5(ct)
        cid = cid.hexdigest()
        cmd = line.strip()
        torun.append([cid,cmd,rerun,debug])
    return torun

def main(cmdfile,threads,rerun,debug):
    print "\nexecuting %s ..." % cmdfile
    torun = parsecmd(cmdfile,rerun,debug)
    pools = Pool(threads)
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
