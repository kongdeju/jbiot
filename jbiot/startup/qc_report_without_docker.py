#!/usr/bin/env python
import sys
import os
dirpath = os.path.join(os.path.dirname(os.path.abspath(__file__)),"../")
sys.path.insert(0,dirpath)
from {{projName}}.arranger.arrange import arrange
from {{projName}}.reporter.report import report 
import yaml
from jbiot import jbiotWorker

# entrypoint function
def {{projName}}(params):

    # call apps

    arrange(params)
    report(params)
    
    return params

# mulit-omics platform
class {{projName}}Worker(jbiotWorker):
    def handle_task(self,key,params):
        self.execute({{projName}},params)


# main function
def main(yml):
    #1. read yaml 
    params = {}
    params["yaml"] = yml
    {{projName}}(params)

if __name__ == "__main__":
    from docopt import docopt
    usage = """
    Usage:
       {{projName}}.py -c <params> 

    Options:
        -c,--conf <params>    params in yaml format.

    """
    args = docopt(usage)
    yml = args["--conf"]
    main(yml)

