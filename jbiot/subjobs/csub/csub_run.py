import os
import yaml
import hashlib
import sys
from multiprocessing import Pool,Process
import subprocess
from ..jblog import jblog
from ..stopjobs import cstop
import signal
import time
import re
pat = re.compile(r"(docker|singularity)[\s\S]+\$PWD\s+(.+?)\s+(.+)")

parent_id = os.getpid()
pid_pat =  re.compile("\((\d+?)\)")
def init_worker():
    def sig_init2(signal_num,frame):
        cstop()
        cmd = "pstree -p %s" % parent_id
        p = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        out = p.stdout.read()
        pids = pid_pat.findall(out)
        pids = set(pids)
        for pid in pids:
            cmd = "kill -9 %s 1>>/dev/null 2>>/dev/null"  % pid
            os.system(cmd)
        cmd = "kill -9 %s 1>>/dev/null 2>>/dev/null" % parent_id
        os.system(cmd)

        pid = os.getpid()
        cmd = "kill -9 %s 1>>/dev/null 2>>/dev/null" % pid
        os.system(cmd)
        sys.exit()
    signal.signal(signal.SIGINT, sig_init2)


cmdstatus = ".status"
def checkstatus(cid):
    if not os.path.exists(cmdstatus):
        os.mkdir(cmdstatus)
    s = os.path.join(cmdstatus,cid+".status")
    if os.path.exists(s):
        return 1
    return 0

cmd_run = "/lustre/users/kongdeju/DevWork/jbiot/jbiot/subjobs/csub/cmd_qsub_run.py"
if not os.path.exists(cmd_run):
    cmd_run = "cmd_qsub_run.py"


def run(cmdfile,mem,cpu,rerun,verbose):
 
    cid = cmdfile.split("/")[-1].split(".")[0]
    cmd = open(cmdfile).read().strip("\n")
    icmd = cmd
    mat = pat.search(cmd)
    if mat :
        icmd = mat.groups()[-1]
    jobid = None
    
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
    logfile = os.path.join(".log","%s.log"%cid)
    os.system("mkdir -p .log")
    fp = open(logfile,"w")
    qcmd = '%s %s --mem %s --cpu %s' % (cmd_run,mem,cpu,cmdfile)
    fp.write(qcmd+"\n\n")
    fp.close()
    if not s:
        p = subprocess.Popen(qcmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        p.wait()
        stdinfo = p.stdout.read()
        steinfo = p.stderr.read()
        if stdinfo:
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
        jobid : %s
        logfile:%s
        """ % (icmd,status,jobid,logfile)

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

def parsecmd(cmdfile):
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
        line = cmd + "\n"
        fp.write(line)
        fp.close()
        torun.append(cmdf)
    return torun


def main(cmdfile,mem,cpu,rerun,verbose):
    jblog("\nexecuting %s ...\n" % cmdfile)
    cmdfiles = parsecmd(cmdfile)
    pools = Pool(len(cmdfiles),init_worker)
    fail = 1
    try:
        ps = []
        for cmdfile in cmdfiles:
            time.sleep(10)
            p = pools.apply_async(run,(cmdfile,mem,cpu,rerun,verbose)) 
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

