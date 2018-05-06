#!/usr/bin/env python

import os
from jinja2 import Template


appt = os.path.join(os.path.dirname(os.path.abspath(__file__)),"app.templ")
curdir = os.getcwd()

def stapp(app):

    # bin/project.py    
    cmd = "mkdir -p %s" % app
    os.system(cmd)

    mc = open(appt).read()
    template =  Template(mc)
    main = template.render(appName=app)
    fp = open(app + "/" + app+".py","w")
    fp.write(main)
    fp.close()
    os.system("touch %s/__init__.py" % app)
    os.chdir(app)
    os.system("ln -s ../config.py ") 
    os.chdir(curdir) 
