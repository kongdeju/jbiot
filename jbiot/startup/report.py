try:
    from config import render
    from config import md2html
except:
    render = "render.py"
    md2html = "md2html.py"
from jbiot import log
import os
from jbiot import jbiotWorker
from jbiot import get_template
from jbiot import yamladd
import yaml
import json

def report(params):
    """ {{projName}} to markdown file and html file

    Args: report input dict, key is `yaml`, value is yaml file path::

            "xx": path of xx.

    Returns:
        dict : key is `yaml`,value is yaml file path
    """
    # handle input
    yamlin = params["yaml"]
    indict = yaml.load(open(yamlin))

    render_yml = "{{projName}}_render.yml"
    cmd = "echo '%s' > %s" % (json.dumps(indict),render_yml)

    templ = get_template("{{projName}}")
    out = "{{projName}}.md"
    cmd = "%s -t %s -j %s -o %s -y" % (render,templ,render_yml,out)
    log.run("render {{projName}} template",cmd,docker="jbioi/report",singularity="report.img")
    
    cmd = "%s %s" % (md2html,out)
    log.run("md2html {{projName}} ",cmd,docker="jbioi/report",singularity="report.img")
    outdict = {}
    outdict["{{projName}}"] = out
    yamlout = yamladd(yamlin,outdict)
    yamlout["{{projName}}_outdir"] = os.getcwd()
    return yamlout

class reportWorker(jbiotWorker):
    def handle_task(self,key,params):
        self.execMyfunc(report,params)

