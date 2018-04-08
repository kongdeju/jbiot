try:
    import config
except:
    pass

from jbiot import jbiotWorker
from jbiot import log
from jbiot import yamladd
import yaml

def arrange(params):
    """ {{projName}} arrange output files

    Args:
        params: indict , key is `yaml`, value in yaml file::

            "xx": path of xx.

    Returns:
        dict : key is `yaml`, value is path of yaml file

    """

    # handle input
    yamlin = params["yaml"]
    indict = yaml.load(open(yamlin).read())
 
    # process cmd and user log.move to arrange files to report
    pass

    # handle output

    #handle out
    outdict = {}
    yamlout = yamladd(yamlin,outdict)
    return yamlout

class {{projName}}Arranger(jbiotWorker):
    def handle_task(self,key,params):
        self.execMyfunc(arrange,params)

