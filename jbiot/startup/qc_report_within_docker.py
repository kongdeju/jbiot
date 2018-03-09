#!/usr/bin/env python
import os
import sys
dirpath = os.path.join(os.path.dirname(os.path.abspath(__file__)))

##################################
# user can define these variables#

img = "kongdeju/alpine-dev:stable"
script = "{{projName}}_without_docker.py"

##################################


     
# DONT CHANGE THE FOWLLOWING CODE#
qp = os.path.join(dirpath,script)

# render soft source path
rootDir = "/jBioTroOtDir"
qp = rootDir + qp

# render current workdir 
curdir = os.getcwd()
curDir = rootDir + curdir

def renderCMD(cmd,rootDir):
    cmdelements = cmd.split()
    for i in range(len(cmdelements)):
        element = cmdelements[i]
        if element.startswith("/"):
            element = rootDir + element
            cmdelements[i] = element
    cmd = " ".join(cmdelements)
    return cmd

def refineCMD(cmd):
    cmd = 'sed -i.backup "s/\%s//g" %s' % (rootDir,cmd)
    os.system(cmd)

def with_docker(img,cmd=""):
    cmd = renderCMD(cmd,rootDir)
    cmd = "docker run --rm -v /:%s  -w %s %s python %s %s  " % (rootDir,curDir,img,qp,cmd)
    os.system(cmd)
    if os.path.exists("run.cmd"):
        refineCMD("run.cmd")


if __name__ == "__main__":
    import sys
    cmd = " ".join(sys.argv[1:])
    with_docker(img,cmd)
