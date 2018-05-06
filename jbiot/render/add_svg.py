import os
from base64 import b64encode

def b64(afile):
    fp = open(afile)
    c = b64encode(fp.read())
    return c

def checkexists(afile):
    if os.path.exists(afile):
        return 1

def render_svg(svg):
    raw = b64(svg)
    cont = """\n<center><iframe src="data:image/svg+xml;base64,%s" width=600 height=600  frameborder="0" > </iframe></center>\n""" % (raw)
    return cont


def add_svg(svg):
    if not svg:
        return "\nno img data\n"

    if type(svg) == str and checkexists(svg):
        img = render_svg(svg)
        return img

    if type(svg) == list and checkexists(svg[0]):
        img = render_svg(svg[0])
        return img

    if type(svg) == dict and checkexists(svg.values()[0]):
        img = render_svg(svg.values()[0])
        return img

    return "\nno img data\n"

