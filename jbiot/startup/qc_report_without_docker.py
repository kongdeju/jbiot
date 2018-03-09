#!/usr/bin/env python
import sys
import os
dirpath = os.path.join(os.path.dirname(os.path.abspath(__file__)),"../")
sys.path.insert(0,dirpath)
from {{projName}}.arranger.arrange import arrange
from {{projName}}.reporter.report import report 
import yaml
from jbiot import jbiotWorker

def {{projName}}(params):

    # call worker1
    indict = {}
    pass 

    # call worker2
    indict = {}
    pass 

    # call arrange
    indict = {}
    
    outdict = arrange(indict)

    # call report
    indict = {}

    indict["render_json"] = outdict["render_json"]
    if "{{projName}}_template" in params:
        indict["{{projName}}_template"] = params["{{projName}}_template"]
    else:
        url = "http://www.genescret.com:6636/templates/{{projName}}_template.md"
        indict["qc_report_template"] = url

    outdict = report(indict)

    # key and value need to write into main yaml
    output = {}
    
    return output

class {{projName}}Worker(jbiotWorker):
    def handle_task(self,key,params):
        self.execute({{projName}},params)

def main(yml):
    #1. read yaml 
    ymlstr = open(yml).read()
    params = yaml.load(ymlstr)
    outputdict = {{projName}}(params)
    
    #2. write yaml
    ystr = yaml.dump(outputdict)
    fp = open(yml,"w")
    fp.write(ymlstr)
    fp.write(ystr)
    fp.close()

if __name__ == "__main__":
    from docopt import docopt
    usage = """
    Usage:
       {{projName}}.py -c <params> 

    Options:
        -c,--conf <params>    params file for soft in yaml format,the following key is needed.

    """
    args = docopt(usage)
    yml = args["--conf"]
    main(yml)

