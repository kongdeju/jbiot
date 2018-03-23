try:
    from config import render
    from config import md2html
except:
    render = "render.py"
    md2html = "md2html.py"

import os
from jbiot import log
from jbiot import jbiotWorker
from jbiot import get_template

def report(params):
    """ convert md to html...

    Args:
        params (dict) : report parmas::

            {
                "render_json" : json file of arrrange.
            }

    Returns:
        dict : report dict::

        {
            "report_md": markdown file which is rendered.

        }

    """

    # handle input
    templ = get_template("{{projName}}")
    ijson = params["render_json"] 

    # process cmd
    out = "{{projName}}.md"
    cmd = "%s -t %s -j %s -o %s" % (render,templ,ijson,out)
    log.run("render mapping {{projName}} template",cmd,docker="kongdeju/alpine-dev:stable")
    
    cmd = "%s %s" % (md2html,out)
    log.run("md2html {{projName}} report ",cmd,docker="kongdeju/alpine-dev:stable")

    # handle output
    outdict = {}
    outdict["report_md"] = out
    return outdict

class reportWorker(jbiotWorker):
    def handle_task(self,key,params):
        self.execMyfunc(report,params)

