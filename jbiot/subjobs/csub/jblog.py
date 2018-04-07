#coding=utf-8
import hashlib
from csub_strip import stripcmd
from csub_run import checkstatus
import time
import os

logdir = ".log"

def checklog(cid):
    logfile = os.path.join(logdir,cid)
   
    if not os.path.exists(logfile):
        return None,"no logs found. \n"

    err = ""
    fp = open(logfile)
    for line in fp.readlines():
        if line.find("Error") != -1 or line.find("error") != -1 or line.find("ERROR") != -1 or line.find("not found") != -1 or line.find(u"无法") != -1 or line.find(u"没有") != -1 or line.find(u"错误") != -1 or line.find(u"未") != -1:
            err = err + line

    return logfile,err

def readlog(cmdfile):

    content = "Job report.\n\n"
    content = content + "working dir : %s\n" % os.getcwd()
    endtime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    content = content + "finished time: %s\n\n" % (endtime)

    content = content + "Details:\n\n"

    tasks = stripcmd(cmdfile)
    i = 0
    for task in tasks:
        i = i + 1
        taskline = "\ntask_%02d:\n" % i
        cmdfile = task[0]
        content = content + taskline
        fp = open(cmdfile)
        ct = cmdfile 
        for line in fp.readlines():
            ct = ct + line
            cid = hashlib.md5(ct)
            cid = cid.hexdigest()
            cmd = line.strip()
            status = checkstatus(cid)
            logfile,err = checklog(cid)
            
            cmdline = cmd + "\n"
            flag = "faild"
            if status: flag = "success"
            statusline = "\tstatus: %s\n" % flag
            errline = "\terror: %s\n" % err
            logline = "\tdetail: %s\n" % logfile
            content = content + cmdline + statusline +  errline + logline
    return content
