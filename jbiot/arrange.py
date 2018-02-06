import os
from logrun2 import log

def arrange(tgtdir,*files):

    if not os.path.exists(tgtdir):
        cmd = "mkdir -p %s" % tgtdir 
        log.run(cmd,cmd)

    filestr = " ".join(files)
    cmd = "cp %s %s" % (filestr,tgtdir)
    log.run("arrange files",cmd)





    
