#!/usr/bin/env python
from cmdPara import cmdPara
from cmdStep import cmdStep
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

def main(cmd,dryflag):
        
    cmdrun = lsub(cmd)
    if dryflag:
        return

    execute(cmdrun)
      

if __name__ == "__main__":
    
    from docopt import docopt

    usage = """
    Usage:
        lsub.py <cmdfile>  [--dry]

    Options:
        -h --help        print this screen
        --dry            all done but run script
    """
    args = docopt(usage) 
    cmdfile = args["<cmdfile>"]
    dryflag = args["--dry"]
    main(cmdfile,dryflag)

   

    
    

