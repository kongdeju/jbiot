import os
from logrun2 import log
url = "http://jbio.cc:6636/dev-report/"

def get_template(projName):

    home = os.environ["HOME"]
    tmpl = "%s_template.md" % projName
    localdir = os.path.join(home,".templates")
    #if not os.path.exists(localdir):
    #    os.mkdir(localdir)
 
    localfile = os.path.join(localdir,tmpl)
    cwdlocalfile  = tmpl

    remote = url + "%s/%s_template.md" % (projName,projName)
    cmd = "wget %s -P %s" % (remote,localdir)
    tag = "get %s tempate" % projName
    log.run(tag,cmd)

    return localfile

