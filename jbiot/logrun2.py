import os
from collections import OrderedDict
import hashlib
import sys

main_name =  sys.argv[0]
main_name = main_name.split("/")[-1].split(".")[0]

hostname = main_name
cfile = hostname + ".cmd"
if os.path.exists(cfile):
    os.system("rm %s" % cfile)

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
    def run(tag,cmd,i=[],o=[],cpu=1,para=1,mem="2G",docker='jbioi/alpine-dev',singularity='alpine-dev.img'):
        cmdfile =  hostname + ".cmd"
        cmdict = load2dict(cmdfile)
        tag = "#### %s: %s --para=%s --cpu=%s --mem=%s --docker=%s --singularity=%s" % (main_name,tag,para,cpu,mem,docker,singularity)
        if i:
            i = ",".join(i)
            icmd = "I=%s" % i
            cmd = cmd + ";    " + icmd
        if o:
            o = ",".join(o)
            ocmd = "O=%s" % o
            cmd = cmd +  ";    " + ocmd

        #dict
        if tag in cmdict:
            cmdict[tag].append(cmd)
        else:
            cmdict[tag] = [cmd]
        dict2cmd(cmdict,cmdfile)


    @staticmethod
    def move(files,tgtdir):

        dircmd = "mkdir -p %s" % tgtdir
        log.run(dircmd,dircmd)
        tag = "copy files to %s" % tgtdir

        if type(files) == dict:
            outs = files.values()
            v = files.values()[0]
            if type(v) == list:
                outs = []
                for its in files.values():
                    outs.extend(its)
            for f in outs:
                cmd = "cp -r %s %s" % (f,tgtdir)
                log.run(tag,cmd)
        
        if type(files) == str:
            cmd = "cp -r %s %s " % (files,tgtdir)
            log.run(tag,cmd)

        if type(files) == list:
            for f in files:
                cmd = "cp -r %s %s" % (f,tgtdir)
                log.run(tag,cmd)
                                                    
def test_log():
    log.run("bwa align","bwa mem hg19.fq test.fq > out.sam")
    log.run("samtool align","bwa mem hg19.fq test.fq > out.sam")
    log.run("1","bwa mem hg19.fq test.fq > out.sam",para=2,i=["ref","alt"],o=[])

if __name__ == "__main__":
    test_log()

