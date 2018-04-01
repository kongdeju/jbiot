import os
import yaml
import hashlib
import sys
from multiprocessing import Pool

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

def run(cid,cmd):
    s = checkstatus(cid)
    if not s:
        flag = os.system(cmd)
        if flag != 0 :
            addstatus(cid)
        else:
            sys.exit()

def parsecmd(cmdfile):
    fp = open(cmdfile)
    ct = cmdfile
    torun = []
    for line in fp.readlines():
        ct = ct + line
        cid = hashlib.md5(ct)
        cid = cid.hexdigest()
        cmd = line.strip()
        torun.append([cid,cmd])
    return torun

def main(cmdfile):
    torun = parsecmd(cmfile)
    p = Pool()
