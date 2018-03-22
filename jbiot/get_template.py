import os
from logrun2 import log
url = "http://www.genescret.com:6636/dev-report/"

def get_template(projName):

    home = os.environ["HOME"]
    tmpl = "%s_template.md" % projName
    localdir = os.path.join(home,".templates") 
    localfile = os.path.join(localdir,tmpl)
    if os.path.exists(localfile):
        return localfile

    remote = url + "%s/%s_template.md" % (projName,projName)
    cmd = "wget %s -P %s" % (remote,localdir)
    tag = "get %s tempate" % projName
    log.run(tag,cmd)

    return localfile

