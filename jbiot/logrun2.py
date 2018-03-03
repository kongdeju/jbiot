import os
from collections import OrderedDict

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
    def run(tag,cmd,para=1,mem="2G",docker='',singularity=''):
        cmdfile =  "run.cmd"
        cmdict = load2dict(cmdfile)
        tag = "#### %s --para=%s --mem=%s --docker=%s --singularity=%s" % (tag,para,mem,docker,singularity)
        if tag in cmdict:
            cmdict[tag].append(cmd)
        else:
            cmdict[tag] = [cmd]
        
        dict2cmd(cmdict,cmdfile)


def test_log():
    log.run("bwa align","bwa mem hg19.fq test.fq > out.sam")
    log.run("samtool align","bwa mem hg19.fq test.fq > out.sam")
    log.run("1","bwa mem hg19.fq test.fq > out.sam",para=2)



if __name__ == "__main__":
    test_log()

