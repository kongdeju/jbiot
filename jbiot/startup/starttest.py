#!/usr/bin/env python

import os
from jinja2 import Template
import sys

appt = os.path.join(os.path.dirname(os.path.abspath(__file__)),"test.templ")


cwd = os.getcwd()
proj = cwd.rstrip("/").split("/")[-2]

def start_test(app):

    # bin/project.py    
    mc = open(appt).read()
    template =  Template(mc)
    main = template.render(projName=proj,appName=app)
    fp = open("test_"+app+".py","w")
    fp.write(main)
    fp.close()
  
