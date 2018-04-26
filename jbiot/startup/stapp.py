#!/usr/bin/env python

import os
from jinja2 import Template


appt = os.path.join(os.path.dirname(os.path.abspath(__file__)),"app.templ")

def stapp(app):

    # bin/project.py    
    mc = open(appt).read()
    template =  Template(mc)
    main = template.render(appName=app)
    fp = open(app+".py","w")
    fp.write(main)
    fp.close()
  
