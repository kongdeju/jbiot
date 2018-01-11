#!/usr/bin/env python
#coding=utf-8
import os

def cmdStep(cmdfile):
    
    prefix = cmdfile.split("/")[-1]

    fp = open(cmdfile)
    lines = fp.readlines()
    step2cmd = {}
    step = 0
    step2cmd[step] = []
    tasks = []
    for line in lines:
        line = line.strip("\n")
        if not line:
            continue

        if line.startswith("#"):
            step = step + 1
            task = line.strip("#").split()[0]
            task = "task.%02d" % (step)
            step2cmd[task]  = [line]
            tasks.append(task)
        else:
            step2cmd[task].append(line)
    
    stepsfile = []
    stepdir = ".steps"
    if not os.path.exists(stepdir):
        os.system("mkdir %s" % stepdir)
    for task in tasks:
        cmds = step2cmd[task]
        if not cmds:
            continue
        scmd = "%s.%s" % (prefix,task)
        scmd = os.path.join(stepdir,scmd)
        fp = open(scmd,"w")
        for cmd in cmds:
            cline = "%s\n" % cmd
            fp.write(cline)
        fp.close()
        stepsfile.append(scmd)

    return stepsfile

if __name__ == "__main__":
    import sys
    from docopt import docopt
    usage = '''
    Usage:
        cmdStep.py <cmdfile> 
        cmdStep.py -h | --help

    Options:
        -h --help                          print this scren

    '''
    args = docopt(usage)
    cmd = args["<cmdfile>"]
    cmdStep(cmd)    


