#!/usr/bin/env python

from pyscaffold.cli import run
import os
from jinja2 import Template

putup = "putup"
setup = os.path.join(os.path.dirname(os.path.abspath(__file__)),"setup.py")
setcfg = os.path.join(os.path.dirname(os.path.abspath(__file__)),"setup.cfg")
travis = os.path.join(os.path.dirname(os.path.abspath(__file__)),".travis.yml")
sphinx_conf = os.path.join(os.path.dirname(os.path.abspath(__file__)),"conf.py")
main_ = os.path.join(os.path.dirname(os.path.abspath(__file__)),"bin.py")
arrange = os.path.join(os.path.dirname(os.path.abspath(__file__)),"arrange.py")
report = os.path.join(os.path.dirname(os.path.abspath(__file__)),"report.py")
gitig = os.path.join(os.path.dirname(os.path.abspath(__file__)),"gitignore")
config = os.path.join(os.path.dirname(os.path.abspath(__file__)),"config.py")
curdir = os.getcwd()

def startup(proj):
    cmd = "putup %s " % proj
    os.system(cmd) 

    # git ignore    
    mc = open(gitig).read()
    template =  Template(mc)
    main = template.render(projName=proj)
    mainpy = "%s/.gitignore" % (proj)
    fp = open(mainpy,"w")
    fp.write(main)
    fp.close()

    os.chdir(proj)
    os.system("git add .")
    os.system("git commit -m 'add ignore'")
    os.chdir(curdir)

    #1. setup.py
    cmd = "cp %s %s/" % (setup,proj)
    os.system(cmd)
    cmd = "cp %s %s/" % (setcfg,proj)
    os.system(cmd)

    #2. travis-ci
    cmd = "cp %s %s/" % (travis,proj) 
    os.system(cmd) 
  
    #3. docs
    cmd = "cp %s %s/docs" % (sphinx_conf,proj)
    os.system(cmd)
    
    # add config.py
    cmd = "cp %s %s/%s" % (config,proj,proj)
    os.system(cmd)

    #4. bin
    cmd = "mkdir -p %s/bin" % proj
    os.system(cmd)

    
    mc = open(main_).read()
    template =  Template(mc)
    main = template.render(projName=proj)
    mainpy = "%s/bin/%s.py" % (proj,proj)
    fp = open(mainpy,"w")
    fp.write(main)
    fp.close()
    cmd = "chmod +x %s/bin/%s.py" % (proj,proj)
    os.system(cmd)

    #5. proj/arranger
    arrdir =  "%s/%s/arranger" % (proj,proj)
    cmd = "mkdir -p %s" % arrdir
    os.system(cmd)
    cmd = "cp %s %s" % (arrange,arrdir)
    os.system(cmd)
    os.chdir(arrdir)
    os.system("touch __init__.py")
    os.system("ln -s ../config.py .")
    os.chdir(curdir)
    #6. proj/reporter
    
    repdir = "%s/%s/reporter" % (proj,proj)
    cmd = "mkdir -p %s " % repdir
    os.system(cmd)

    mc = open(report).read()
    template =  Template(mc)
    main = template.render(projName=proj)
    mainpy = "%s/%s/reporter/report.py" % (proj,proj)
    fp = open(mainpy,"w")
    fp.write(main)
    fp.close()
    
    os.chdir(repdir)
    os.system("touch __init__.py")
    os.system("ln -s ../config.py .")
    os.chdir(curdir)

    #7. gitignore tests/ config

    mc = open(gitig).read()
    template =  Template(mc)
    main = template.render(projName=proj)
    mainpy = "%s/.gitignore" % (proj)
    fp = open(mainpy,"w")
    fp.write(main)
    fp.close() 
    
    os.chdir(proj)
    os.system("rm tests/conftest.py && rm tests/test_skeleton.py")
    os.chdir(proj)
    os.system("rm skeleton.py")
    os.chdir(curdir)
  
    os.chdir(proj)
    os.system("git add . -A") 
    os.system("git commit -m 'init my project'") 
    #8. git remote add  
    os.system("git remote add origin git@123.57.226.13:/expan/DevRepos/%s.git"%proj)
    
if __name__ == "__main__":
    import sys
    startup(sys.argv[1]) 
