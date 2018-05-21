try:
    import config
except:
    pass

from jbiot import jbiotWorker
from jbiot import log
from jbiot import yamladd
import yaml

def arrange(ymlfile):
    """ {{projName}} arrange output files use log.run

    """

    # handle input
    indict = yaml.load(open(ymlfile).read())
 
    # process cmd and user log.move to arrange files to report
    pass

    # handle output

    #handle out
    outdict = {}
    yamladd(ymlfile,outdict)
    return ymlfile

