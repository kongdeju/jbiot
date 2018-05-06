import hashlib
from collections import OrderedDict
import re
import os
docker_pat = re.compile("--docker[= ](.+?) ")
cpu_pat = re.compile("--cpu[= ](\d+?) ")
mem_pat = re.compile("--mem[= ](.+?) ")


def profilecmd(cmdfile):
    docker = "jbioi/alpine-dev"
    cpu = 1
    mem = "2G"
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
            mat = mem_pat.search(taskname)
            if mat: mem = mat.group(1)   
            mat = docker_pat.search(taskname) 
            if mat: docker = mat.group(1)
            mat = cpu_pat.search(taskname)
            if mat: cpu = mat.group(1)
            taskdict[taskname] = [[cpu,mem,docker]]
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
        cpu,mem,docker = cmds[0]
        for cmd in cmds[1:]:
            cmd = cmd + "\n"
            fp.write(cmd)
        fp.close()
        i = i + 1
        tasks.append([taskname,[cpu,mem,docker]])
    return tasks

def stripcmd(cmdfile):
    taskdict = profilecmd(cmdfile)
    tasks = gentask(taskdict)
    return tasks
