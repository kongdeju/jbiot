#!/usr/bin/env python
import os
import sys
import subprocess

dirpath = os.path.join(os.path.dirname(os.path.abspath(__file__)))
withinDocker = os.path.join(dirpath,"{{projName}}_within_docker.py")
withoutDocker = os.path.join(dirpath,"{{projName}}_without_docker.py")

def testlocal():
    cmd = "%s -h" % withoutDocker
    p = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    std = p.stdout.read()
    err = p.stderr.read()
    if err:
        return 
    return 1


def main(argv):
    local = testlocal()
    argv = " ".join(argv)
    if local:   
        print "\nCode environments satisfied. Run without Docker...\n" 
        cmd = "%s %s" % (withoutDocker,argv)
    else:
        print "\nCode environments not satisfied. Run with Docker ...\n" 
        cmd = "%s %s" % (withinDocker,argv)
    os.system(cmd)
    print "\n"
if __name__ == "__main__":
    import sys
    main(sys.argv[1:])
