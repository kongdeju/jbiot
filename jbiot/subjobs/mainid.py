import os

def mainid ():
    pid = os.getpid()
    cmd = "mkdir -p .jids"
    os.system(cmd)
    fp = open(".jids/main.pid","w")
    line = "%s" % pid
    fp.write(line)
    fp.close()
