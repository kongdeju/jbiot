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

def report(ymlfile):
    """ {{projName}} to markdown file and html file

    """
    # handle input
    indict = yaml.load(open(ymlfile))

    render_yml = "{{projName}}_render.yml"
    cmd = "echo '%s' > %s" % (json.dumps(indict),render_yml)
    log.run("get {{projName}} args to render",cmd)

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
    return ymlfile

