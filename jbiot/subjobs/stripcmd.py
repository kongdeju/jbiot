import hashlib
from collections import OrderedDict
#import re
#para_pat = re.compile("--para[= ](\d+)")

def profilecmd(cmdfile):
    i = 1
    cmddict = {}
    content = ""
    fp = open(cmdfile)
    taskdict = OrderedDict()
    for line in fp.readlines():
        line = line.strip()
        if not line: 
            continue
        if line.startswith("#"):
            taskname = "task-%s:%s" % (i,line) 
            #mat = para_pat.search(taskname)
            #para = 1
            #if mat: para = int(mat.group(1))      
            taskdict[taskname] = []
            i = i + 1
            continue
        content = content + line
        m5 = hashlib.md5(content)
        m5 = m5.hexdigest()
        cmddict[m5] = line
        taskdict[taskname].append(m5)
    return cmddict,taskdict

def gentask(taskdict,cmddict):
    i = 1
    for task,cids in taskdict.items():
        taskname = 'task_%02d.cmd' % i
        fp = open(taskname,"w")
        for cid in cids:
            cmd = cmddict[cid]
            cid = "#%s\n" % cid
            fp.write(cid)
            cmd = cmd + "\n"
            fp.write(cmd)
        fp.close()
        i = i + 1

def stripcmd(cmdfile):
    cmddict,taskdict = profilecmd(cmdfile)
    gentask(taskdict,cmddict)

    
