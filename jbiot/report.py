import os
dirpath = os.path.dirname(os.path.abspath(__file__))
render = os.path.join(dirpath,"render.py")
md2html = os.path.join(dirpath,"md2html.py")

from logrun2 import log
from jbiotWorker import jbiotWorker
from get_template import get_template

def report(params):
    """render template and covert md2html
    
    Args:
        params : input dict, which has following keys::

            {
                "proj_name"  : the name of this project,use this name to get the conresponding template.
                "render_json": the input render json .
                "style"      : the style of html. this is optional
            }

    Returns:
        dict : md which is rendered by render_json

    """

    # handle input
    projName = params["projname"]
    ijson = params["render_json"]
    templ = get_template(projName)
    style = None
    if params.has_key("style")
        style = params["style"]
   
    # process cmd 
    out = "%s.md" % projName
    cmd = "%s -t %s -j %s -o %s" % (render,templ,ijson,out)
    tag = "render %s template" % projName

    log.run(tag,cmd,docker="kongdeju/alpine-dev:stable")
    
    
    cmd = "%s %s" % (md2html,out)
    if style:
        cmd = "%s %s -s %s" % (md2html,out,style)

    tag = "md2html %s" % projName
    log.run(tag,cmd,docker="kongdeju/alpine-dev:stable")

    # handle output
    outdict = {}
    outdict["report_md"] = out
    return outdict

class reportWorker(jbiotWorker):
    def handle_task(self,key,params):
        self.execMyfunc(report,params)
