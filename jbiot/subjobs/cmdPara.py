#!/usr/bin/env python
from docopt import docopt
import re
import os
pat1 = re.compile("--para[= ](\d+)")

usage = """


    Usage:
      cmdPara.py <cmdfile> 
      cmdPara.py --version

    Options:
      -h --help                   Show this screen.
      --version                   Show version.

        """

def cmdPara(stepfile):
    threads = 1
    fp = open(stepfile)
    
    cmds =  []
    for line in fp.readlines():
        line = line.strip()
        if not line :
            continue
        if line.startswith("#"):
            mat = pat1.search(line)
            if mat:
                threads = int(mat.group(1))
            continue
        cmds.append(line)

    paradir = ".para"
    if not os.path.exists(paradir):
        os.system("mkdir %s" % paradir)
    parafile = stepfile.split("/")[-1] + ".para"
    parafile = os.path.join(paradir,parafile)
    fp = open(parafile,"w")
    for i in range(len(cmds)):
        cmd = cmds[i]
        cmdlog = stepfile + "_%s.log" % (i+1)
        cmdecho = '''echo executing... "%s" ''' % cmd
        cmdecho = cmdecho + "\n"
        if cmd.strip().startswith("for "):
            cmd = cmd + "\n"
        else:
            if not cmd.startswith("cd"):
                cmd = "echo %s 1>>%s 2>>%s;nohup %s 1>>%s 2>>%s & \n" % (cmd,cmdlog,cmdlog,cmd,cmdlog,cmdlog)
            else:
                cmd = '''echo "%s" ; %s 1 2  \n''' % (cmd,cmd)
        fp.write(cmdecho)
        fp.write(cmd)
        j =  i + 1
        if j % threads == 0:
            line = "wait\n"
            fp.write(line)
    fp.write(line)
    fp.close()
    return parafile

if __name__ == "__main__":

    args = docopt(usage)

    cmdfile = args["<cmdfile>"]
    lsub(cmdfile)
