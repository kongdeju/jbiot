
def csub(stepfile,mem="2G"):
    
    fp = open(stepfile)
    
    cmds =  []
    for line in fp.readlines():
        line = line.strip()
        if not line :
            continue
        if line.startswith("#"):
            continue
        cmds.append(line)

    prex = stepfile.split("/")[-1].split(".")[0]

    for i in range(len(cmds)):
        qjob = prex + ".%s.qsub" % i
        cmd = cmds[i]
        line = """#!/bin/bash 
#$ -S /bin/bash
#$ -cwd
#$ -l vf=%s
date
%s
date
        """ % (mem,cmd)
        fp = open(qjob,"w")
        fp.write(line)
        fp.close()



