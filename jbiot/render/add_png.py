import xlrd
import os
from base64 import b64encode
from PIL import Image

def b64(afile):
    fp = open(afile)
    c = b64encode(fp.read())
    return c

def getName(afile):
    name = afile.split("/")[-1].rsplit(".",1)[0]
    return name

def checkexists(afile):
    if os.path.exists(afile):
        return 1

def getimgsize(image):
    w = 600
    img = Image.open(image)
    width = img.size[0]
    height = img.size[1]

    ratio = float(width) / float(height)

    h = int(w / ratio)
    return (w,h)

def render_png(png):
    w,h = getimgsize(png)
    raw = b64(png)
    cont = '\n<center><img src="data:image/png;base64,%s" width=%s height=%s></center>\n' % (raw,w,h)
    return cont

def add_png(png):
    if not png:
        return "\nno img data\n"

    if type(png) == list:
        png = png[0]

    if type(png) == dict:
        png = png.values()[0]

    if type(png) == str and checkexists(png):
        img = render_png(png)
        return img


    return "\nno img data\n"

