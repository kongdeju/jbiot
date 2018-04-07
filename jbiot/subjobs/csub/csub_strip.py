import hashlib
from collections import OrderedDict
import re
import os
mem_pat = re.compile("--mem[= ](\d+)")

def profilecmd(cmdfile):
    i = 1
    cmddict = {}
    content = ""
    fp = open(cmdfile)
    taskdict = OrderedDict()
    for line in fp.readlines():
        line = line.strip()
        if not line: 
            continue
        if line.startswith("#"):
            taskname = "task-%s:%s" % (i,line) 
            mat = mem_pat.search(taskname)
            mem = "2G"
            if mat: mem = mat.group(1)   
            taskdict[taskname] = [mem]
            i = i + 1
            continue
        cmd = line
        taskdict[taskname].append(cmd)
    return taskdict

def gentask(taskdict):
    tdir = ".task"
    if not os.path.exists(tdir):
        os.mkdir(tdir)
    tasks = []
    i = 1
    for task,cmds in taskdict.items():
        taskname = 'task_%02d.cmd' % i
        taskname = os.path.join(tdir,taskname)
        fp = open(taskname,"w")
        para = cmds[0]
        for cmd in cmds[1:]:
            cmd = cmd + "\n"
            fp.write(cmd)
        fp.close()
        i = i + 1
        tasks.append([taskname,para])
    return tasks

def stripcmd(cmdfile):
    taskdict = profilecmd(cmdfile)
    tasks = gentask(taskdict)
    return tasks
