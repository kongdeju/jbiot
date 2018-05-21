#!/usr/bin/env python
import sys
import os
dirpath = os.path.join(os.path.dirname(os.path.abspath(__file__)),"../")
sys.path.insert(0,dirpath)
from {{projName}}.arranger.arrange import arrange
from {{projName}}.reporter.report import report 

# entrypoint function
def {{projName}}(ymlfile):

    # call apps

    arrange(ymlfile)
    report(ymlfile)
    
    return ymlfile


def main():
    


if __name__ == "__main__":
    from docopt import docopt
    usage = """
    Usage:
       {{projName}}.py -c <params> 

    Options:
        -c,--conf <params>    params in yaml format.
        -e,--exec <method>    method default is off. and can be set one of [sh|lsub|csub|asub]
    """
    args = docopt(usage)
    yml = args["--conf"]
    main(yml)

