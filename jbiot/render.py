#!/usr/bin/python
#coding=utf-8
from jinja2 import Template
import json
import os
import sys
import base64
import xlrd
reload(sys)
sys.setdefaultencoding('utf-8')
from PIL import Image
import yaml
dirpath = os.path.dirname(os.path.abspath(__file__))
macro = os.path.join(dirpath,"func.macro")

def getimgsize(image):
    w = 600
    img = Image.open(image)
    width = img.size[0]
    height = img.size[1]
    
    ratio = float(width) / float(height)

    h = int(w / ratio)
    return (w,h)

def render(tpl,ijson,out,yml):
   
    fcont = open(tpl).read()
    fim = open(macro)
    im = fim.read()
    im = "%s\n" % im
    fcont = im + fcont
    temp = Template(fcont)
    temp.globals['open'] = open
    temp.globals['base64'] = base64.b64encode
    temp.globals["xlrd"] = xlrd
    temp.globals["getimgsize"] = getimgsize
    if yml:
        args = yaml.load(open(ijson).read())
    else:
        args = json.loads(open(ijson).read())
    tmd = temp.render(**args)
    
    fp = open(out,"w")
    fp.write(tmd)
    fp.close()

    return tmd 

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


