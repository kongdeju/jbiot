try:
    import config
except:
    pass

from jbiot import jbiotWorker

def arrange(params):
    """ arrange outfile to destination directory 

    Args:
        params (dict):

    Returns:
        dict : 
    """
    # copy files to report



    # output json file to report
    outdict = {}
    ystr = json.dumps(outdict)
    oj = "{{projName}}.json"
    
    cmd = "echo '%s' > %s " % (ystr,oj)
    tag = "export {{projName}} to jsonfile"
    log.run("tag",cmd)
    out = {}
    out["render_json"] = oj
    return out

class {{projName}}Arranger(jbiotWorker):
    def handle_task(self,key,params):
        self.execMyfunc(arrange,params)

