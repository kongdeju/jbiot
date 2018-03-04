#!/usr/bin/env python
import sys
import os

dirname = os.path.dirname(os.path.abspath(__file__))
dirname = os.path.join(dirname,"../")
sys.path.insert(0,dirname)
from {{projName}}.arranger.arrange import arrange
from {{projName}}.reporter.report import report
from jbiot import jbiotWorker
import yaml

def {{projName}}(indict):
    """introducton to this function
    
    Arags:
        indict: (dict)  description...

    Return:
        dict : description ....
    """ 
    outdict = {}
    return outdict

class qcWorker(jbiotWorker):
    def handle_task(self,key,params):
        self.execMyfunc({{projName}},params)

def main(yml):
    fp = open(yml)
    indict = yaml.load(fp)
    outdict = {{projName}}(indict)
    fp = open(yml,"w") 
    yaml.dump(outdict,default_flow_style=False)   
    return yml

if __name__ == "__main__":

    usage = '''
Usage:
    {{projName}}.py -c <yml>
    {{projName}}.py -h | --help
    {{projName}}.py -v | --version

Options:
    -h --help                         print usage
    -v --version                      print version information
    -c --conf <yml>                   yaml file generated in required format
    '''   

    from docopt import docopt
    args = docopt(usage) 
    yml = args["--conf"]
    main(yml) 

