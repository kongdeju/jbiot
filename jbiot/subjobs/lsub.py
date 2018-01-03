
def lsub(stepfile,threads=1):
    
    fp = open(stepfile)
    
    cmds =  []
    for line in fp.readlines():
        line = line.strip()
        if not line :
            continue
        cmds.append(line)

    prex = stepfile.split("/")[-1].split(".")[0]
    parafile = prex + ".para.cmd"

    fp = open(parafile,"w")
    for i in range(len(cmds)):
        cmd = cmds[i]
        cmdlog = prex + ".%s.log" % i
        cmd = "nohup %s 1>>%s 2>>%s & \n" % (cmd,cmdlog,cmdlog)
        fp.write(cmd)
        j =  i + 1
        if j % threads == 0:
            line = "wait\n"
            fp.write(line)
    line = "wait\n"
    fp.write(line)
    fp.close()
