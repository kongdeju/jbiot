import os

def logrun(cmd,info="cmd info",prefix="run",run=False,docker=False):

    cmdfile = prefix + ".cmd"
    logfile = prefix + ".log"
    fp = open(cmdfile,"a")

    cmdtitle = "### %s\n" % info
    cmd = "    %s 1>>%s 2>>%s " % (cmd,logfile,logfile)
    print
    print cmdtitle
    print cmd
    print
    fp.write("\n")
    fp.write(cmdtitle)
    line = cmd + "\n\n"
    fp.write(line)

    fp.close()

    if run:

        os.system(cmd)


def test_logrun():

    cmd = "bwa mem "
    
    logrun(cmd)


if __name__ == "__main__":
    test_logrun()

    
    

    
