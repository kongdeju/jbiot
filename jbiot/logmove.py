import os
from logrun2 import log

def logmove(files,tgtdir):
    
    dircmd = "mkdir -p %s" % tgtdir
    log.run(dircmd,dircmd)
    tag = "copy files to %s" % tgtdir

    if type(files) == dict:
        files = files.values()
    
    if type(files) == str:
        cmd = "cp %s %s " % (files,tgtdir)
        log.run(tag,cmd)

    if type(files) == list:
        for f in files:
            cmd = "cp %s %s" % (f,tgtdir)
            log.run(tag,cmd)
