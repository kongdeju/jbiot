import os
import subprocess

def checkbcs():
    bcs = 0
    home = os.environ["HOME"]
    cfg = ".batchcompute/cliconfig"
    cfg = os.path.join(home,cfg)
    if os.path.exists(cfg) : 
        lines = open(cfg).readlines()
        if len(lines) >= 7:
            bcs = 1

    info = """
        bcs needs inilization...
        
            \033[1;32mtype bcs set -h.\033[0m

    """
    if not bcs:
        print info

    return bcs


def checkdcs():
    
    dcs = 0
    cmd = "ps aux | grep docker-proxy-current | grep 8864 | grep 5000"
    p = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    p.wait()
    lines = p.stdout.readlines()
    for line in lines:
        if line.find("grep") == -1:
            dcs = 1
            break

    info = """
    docker registry service needs to set.

        \033[1;32mhttps://help.aliyun.com/document_detail/28022.html?spm=a2c4g.11186623.6.572.4kpHYv

                                            or 

                        use dcs-start to start ali docker service\033[0m
         
    """

    if not dcs:
        print info

    return dcs



if __name__ == "__main__":
    checkdcs()
