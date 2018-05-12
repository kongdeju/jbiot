import os
import sys

cfg = os.path.join( os.path.dirname(os.path.abspath(__file__)), "config.yml")

def dcs():
    
    cmd = "docker run -v %s:/etc/docker/registry/config.yml -p 8864:5000 --name registry -d registry:2" % cfg
    print cmd
    os.system(cmd)


