import os
import sys

name = sys.argv[0].split("/")[-1].split(".")[0]
logfile = "%s.log" % name

def jblog(text):
    origin = sys.stdout
    print text
    fp = open(logfile,"a")
    sys.stdout = fp
    text = text.replace("\033[0m","")
    text = text.replace("\033[1;33m","")
    text = text.replace("\033[1;32m","")
    text = text.replace("\033[1;31m","")
    print text
    sys.stdout = origin



def readlog():
    fp = open(logfile)
    return fp.read()


if __name__ == "__main__":
    jblog("hello")



