from docopt import docopt

usage = """


    Usage:
      naval_fate.py <cmdfile> [-j <num>]
      naval_fate.py --version

    Options:
      -h --help                   Show this screen.
      --version                   Show version.
      -j=<K> --parallel=<K>       threads [default: 1]


        """

def lsub(stepfile,threads=1):
   
    threads = int(threads) 
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


if __name__ == "__main__":

    args = docopt(usage)

    cmdfile = args["<cmdfile>"]
    threads = args["--parallel"] 
    lsub(cmdfile,threads)
