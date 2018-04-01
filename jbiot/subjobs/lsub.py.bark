#!/usr/bin/env python
from cmdPara import cmdPara
from cmdStep import cmdStep
from dockersing import dockersing
import os

def lsub(cmd):
    
    cmdfiles = cmdStep(cmd)
    cmdparas = []
    for cmdfile in cmdfiles:
        cmdpara = cmdPara(cmdfile)
        cmdparas.append(cmdpara)

    cmdrun  = cmd+".sh"
    fp = open(cmdrun,"w") 
    
    for para in cmdparas:
        
        line = "sh %s\n" % para
        fp.write(line)
    fp.close()
    os.system("chmod +x %s" % cmdrun)
    return cmdrun

def execute(cmd):

    log = cmd + ".log"
    sh =  "sh %s" % (cmd)
    os.system(sh)

def main(cmd,dryflag,docker=False,sing=False):
    if docker:
        cmd = dockersing(cmd,prefer="docker")
    if sing:
        cmd = dockersing(cmd,prefer="singularity")
    cmdrun = lsub(cmd)
    if dryflag:
        return

    execute(cmdrun)
      

if __name__ == "__main__":
    
    from docopt import docopt

    usage = """
    Usage:
        lsub.py <cmdfile>  [--dry] [--with-docker|--with-singularity]

    Options:
        -h --help           print this screen
        --dry               all done but run script
        --with-docker       prefer to use docker when run cmd
        --with-singularity  prefer to user singularity when run cmd

    """
    args = docopt(usage) 
    cmdfile = args["<cmdfile>"]
    dryflag = args["--dry"]
    docker = args["--with-docker"]
    sing = args["--with-singularity"]
    main(cmdfile,dryflag,docker=docker,sing=sing)

   

    
    

