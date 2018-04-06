#!/usr/bin/env python

import sys
import os
dirpath = os.path.join(os.path.dirname(os.path.abspath(__file__)),"../")
sys.path.insert(0,dirpath)

from jbiot.render.render import render

if __name__ == "__main__":
    import sys
    from docopt import docopt
    usage = """
    Usage:
        render.py -t <template> -j <ijson> -o <output> [-y]

    Options:
        -t <template> --template=<template>      tempate to render
        -j <json> --json=<ijson>                 args json dict or ya
        -o <out> --out=<out>                     output
        -y, --yaml                               yaml input
    
    """
    args = docopt(usage)
    tp = args["--template"]
    ij = args["--json"]
    ot = args["--out"]
    yml = args["--yaml"]
    render(tp,ij,ot,yml)


