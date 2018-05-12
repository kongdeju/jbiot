import os
import subprocess

def deamon(script,argstr,cmdfile,stop):

    cmd = "nohup %s %s 1>>/dev/null 2>>/dev/null &" % (script,argstr)
    p = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,preexec_fn=os.setpgrp)
    pid = p.pid
    if not os.path.exists(".jids"):
        os.system("mkdir -p .jids")

    fp = open(".jids/deamon.pid","w")
    line = "%s" % pid
    fp.write(line)
    fp.close()

    fp = open("stopmyjob.sh","w")
    line = "%s\n" % stop
    fp.write(line)
    fp.close()
    os.system("chmod +x stopmyjob.sh")

    logfile = cmdfile.split("/")[-1].split(".")[0] + ".log"
    print "\nRun in deamon mode..."
    print "\t status   : \033[1;32mrunning\033[0m"
    print "\t check log: %s" % logfile
    print "\t stop job : sh stopmyjob.sh\n"

