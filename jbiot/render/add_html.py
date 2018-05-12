import os
from base64 import b64encode

def b64(afile):
    fp = open(afile)
    c = b64encode(fp.read())
    return c

def checkexists(afile):
    if os.path.exists(afile):
        return 1

def render_html(html):
    raw = b64(html)
    cont = """\n<center><iframe src="data:text/html;base64,%s" width=600 height=600  frameborder="0" > </iframe></center>\n""" % (raw)
    return cont


def add_html(html):
    if not html:
        return "\nno img data\n"

    if type(html) == str and checkexists(html):
        img = render_html(html)
        return img

    
    if type(html) == list and checkexists(html[0]):
        img = render_html(html[0])
        return img

    if type(html) == dict and checkexists(html.values()[0]):
        img = render_html(html.values()[0])
        return img
 

    return "\nno img data\n"

