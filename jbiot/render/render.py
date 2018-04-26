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
dirpath = os.path.dirname(os.path.abspath(__file__))
macro = os.path.join(dirpath,"func.macro")
from PIL import Image
import yaml
from add_text import add_text
from add_xls import add_xls
from add_png import add_png
from add_png import getName
from add_png import b64 as baseimg
from add_png import getimgsize
from add_pdf import pdfs2pngs 
from add_pdf import add_pdf
from add_pngs import handle_pngs
from add_tsv import add_tsv
from add_svg import add_svg
from add_html import add_html

def render(tpl,ijson,out,yml):
    mac = open(macro).read()
    fcont = open(tpl).read()
    fcont = mac + "\n\n" + fcont 
    temp = Template(fcont)
    temp.globals["add_text"] = add_text
    temp.globals["add_xls"] = add_xls
    temp.globals["add_png"] = add_png
    temp.globals["baseimg"] = baseimg
    temp.globals["getimgsize"] = getimgsize
    temp.globals["getName"] = getName
    temp.globals["pdfs2pngs"] = pdfs2pngs
    temp.globals["add_pdf"] = add_pdf
    temp.globals["handle_pngs"] = handle_pngs
    temp.globals["add_tsv"] = add_tsv
    temp.globals["add_svg"] = add_svg
    temp.globals["add_html"] = add_html
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
