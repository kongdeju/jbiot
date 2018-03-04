try:
    import config
except:
    pass

import json
from jbiot import jbiotWorker

def arrange(params):
    """ arrange outfile to destination directory 

    Args:
        params (dict):

    Returns:
        dict : 
    """
    # params to outdict to json

    outdict = {}
    ystr = json.dumps(outdict)
    oj = "args.json"
    fp = open(oj,"w")
    fp.write(ystr)
    fp.close()

    out = {}
    out["render_json"] = oj
    return out

class qcArranger(jbiotWorker):
    def handle_task(self,key,params):
        self.execMyfunc(arrange,params)


