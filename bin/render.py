#!/usr/bin/env python

import sys
import os
dirpath = os.path.join(os.path.dirname(os.path.abspath(__file__)),"../")
sys.path.append(dirpath)

from jbiot.render import render

if __name__ == "__main__":
    import sys
    from docopt import docopt

    usage = """
    Usage:
        render.py -t <template> -j <ijson> -o <output>

    Options:
        -t <template> --template=<template>      tempate to render
        -j <json> --json=<ijson>                 args json dict
        -o <out> --out=<out>                     output
        
    """
    args = docopt(usage)
    tp = args["--template"]
    ij = args["--json"]
    ot = args["--out"]
    render(tp,ij,ot)


