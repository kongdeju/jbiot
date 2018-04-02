import os
from collections import OrderedDict
hostname = os.environ["HOSTNAME"]
import hashlib

def load2dict(cmdfile):
    dic = OrderedDict()
    if not os.path.exists(cmdfile):
        return dic
    fp = open(cmdfile)
    lines = fp.readlines()
    fp.close()
    for line in lines:
        line = line.strip()
        if not line:
            continue
        if line.startswith("#"):
            tag = line
            dic[tag] = []
        else:
            dic[tag].append(line)
    return dic


def dict2cmd(dic,cmdfile):
    fp = open(cmdfile,"w")
    for k,cmds in dic.items():
        line = "\n" +  k + "\n\n"
        fp.write(line)
        for cmd in cmds:
            cmd = "    %s\n" % cmd
            fp.write(cmd)
    fp.close()
    
class log:
    @staticmethod
    def run(tag,cmd,i=[],o=[],para=1,mem="2G",docker='jbioi/alpine-dev',singularity='alpine-dev.img'):
        cmdfile =  hostname + ".cmd"
        iocmdfile =  hostname + ".ali.cmd"
        cmdict = load2dict(cmdfile)
        iocmdict = load2dict(iocmdfile)
        tag = "#### %s --para=%s --mem=%s --docker=%s --singularity=%s" % (tag,para,mem,docker,singularity)
        icmd = "I=unknown"
        if i:
            i = ",".join(i)
            icmd = "I=%s" % i
        ocmd = "O=unknown"
        if o:
            o = ",".join(o)
            ocmd = "O=%s" % o
        iocmd = cmd + ";     " + icmd + ";" + ocmd

        #dict
        if tag in cmdict:
            cmdict[tag].append(cmd)
        else:
            cmdict[tag] = [cmd]
        dict2cmd(cmdict,cmdfile)

        #iodict        
        if tag in iocmdict:
            iocmdict[tag].append(iocmd)
        else:
            iocmdict[tag] = [iocmd]
        dict2cmd(iocmdict,iocmdfile)


def test_log():
    log.run("bwa align","bwa mem hg19.fq test.fq > out.sam")
    log.run("samtool align","bwa mem hg19.fq test.fq > out.sam")
    log.run("1","bwa mem hg19.fq test.fq > out.sam",para=2)

if __name__ == "__main__":
    test_log()

