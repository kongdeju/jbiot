try:
    from config import render
except:
    render = "render.py"
from jbiot import log
import os
from jbiot import jbiotWorker

def report(params):
    templ = params["{{projName}}_template"]
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


