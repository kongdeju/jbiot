try:
    from config import render
except:
    render = "render.py"
from jbiot import log
import os
from jbiot import jbiotWorker

def get_file(remotefile):
    home = os.environ["HOME"]
    localfile = remotefile.split("/")[-1]
    cmd = "wget %s -P ~/.report_templates " % (remotefile)
    localpath = os.path.join(home,".report_templates",localfile)
    if os.path.exists(localpath):
        return localpath
    os.system(cmd)
    
    return localpath

def report(params):
    # get template
    templ = params["{{projName}}_template"]
    if templ.startswith("http://"):
        templ = get_file(templ)


    ijson = params["render_json"] 
    out = "{{projName}}.md"
    cmd = "%s -t %s -j %s -o %s" % (render,templ,ijson,out)
    log.run("render mapping template",cmd)

    outdict = {}
    outdict["report_md"] = out
    return outdict


class reportWorker(jbiotWorker):
    def handle_task(self,key,params):
        self.execMyfunc(report,params)


