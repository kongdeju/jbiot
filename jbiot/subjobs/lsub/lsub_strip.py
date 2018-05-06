import hashlib
from collections import OrderedDict
import re
import os
para_pat = re.compile("--para[= ](\d+)")

def profilecmd(cmdfile):
    i = 1
    cmddict = {}
    content = ""
    fp = open(cmdfile)
    taskdict = OrderedDict()
    lines = fp.readlines()
    name = "###" + cmdfile.split("/")[-1].split(".")[0]
    lines.insert(0,name)
    for line in lines:
        line = line.strip()
        if not line: 
            continue
        if line.startswith("#"):
            taskname = "task-%s:%s" % (i,line) 
            mat = para_pat.search(taskname)
            para = 1
            if mat: para = int(mat.group(1))      
            taskdict[taskname] = [para]
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
        if len(cmds) == 1:
            continue
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
