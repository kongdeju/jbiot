import os
import time

def setwdir(wdir):
    os.system("mkdir -p .task")
    fp = open(".task/wdir","w")
    fp.write(wdir)
    fp.close()
    

def readwdir():

    ftime = time.strftime('%Y-%m-%d-%H-%M-%S',time.localtime(time.time()))
    wdir = "oss://jbiobio/working/tmp/%s/" % ftime
    if  os.path.exists(".task/wdir"):
        fp = open(".task/wdir")
        wdir = fp.read().strip()
    return wdir
