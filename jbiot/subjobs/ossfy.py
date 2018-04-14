import os
from alisub.ossio.oss2tools import osslist

def osscmd(cmd):
    osscmds = []    
    cmditems = cmd.split()
    for i in range(len(cmditems)):
        item = cmditems[i]
        if item.startswith("oss://"):
            item = item.strip("/")
            localfile = item.split("/")[-1]
            if not os.path.exists(localfile):
                osscmd = "oss2tools.py download %s . " % (item)
                osscmds.append(osscmd)
            
            item = item.split("/")[-1]
            cmditems[i] = item
    cmd = " ".join(cmditems)
    return osscmds,cmd


def ossfy(cmdfile):

    lines = open(cmdfile).readlines()
    osscmdfile = cmdfile.rsplit(".",1)[0] + ".oss.cmd"
    fpw = open(osscmdfile,"w")
    osslines = []
    for line in lines:
        line = line.strip()
        if not line.startswith("#"):
            osscmds,line = osscmd(line)
            osslines.extend(osscmds)
            line = "\t" + line
        line = line +" \n" 
        fpw.write(line)
    fpw.close()

    # handle ossfiles
    osslines  = set(osslines)
    if osslines:
        print "\ndownloading oss files...\n"
    for ossline in osslines:
        print "\t" + ossline
        os.system(ossline)
    return osscmdfile


if __name__ == "__main__":
    
    import sys
    cmdfile = sys.argv[1]
    ossfy(cmdfile)


