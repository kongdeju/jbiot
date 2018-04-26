#!/usr/bin/env python
#coding=utf-8
import os
from jinja2 import Template
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

putup = "putup"
setup = os.path.join(os.path.dirname(os.path.abspath(__file__)),"setup.py")
setcfg = os.path.join(os.path.dirname(os.path.abspath(__file__)),"setup.cfg")
travis = os.path.join(os.path.dirname(os.path.abspath(__file__)),".travis.yml")
sphinx_conf = os.path.join(os.path.dirname(os.path.abspath(__file__)),"conf.py")
arrange = os.path.join(os.path.dirname(os.path.abspath(__file__)),"arrange.py")
report = os.path.join(os.path.dirname(os.path.abspath(__file__)),"report.py")
gitig = os.path.join(os.path.dirname(os.path.abspath(__file__)),"gitignore")
config = os.path.join(os.path.dirname(os.path.abspath(__file__)),"config.py")
curdir = os.getcwd()

maindocker = os.path.join(os.path.dirname(os.path.abspath(__file__)),"qc_report_within_docker.py")
main_ = os.path.join(os.path.dirname(os.path.abspath(__file__)),"qc_report.py")
raw = os.path.join(os.path.dirname(os.path.abspath(__file__)),"qc_report_without_docker.py")
sdir = os.path.dirname(os.path.abspath(__file__))

def render(tmp,tgt,proj):
    mc = open(tmp).read()
    template = Template(mc)
    rc = template.render(projName=proj)
    fp = open(tgt,"w")
    fp.write(rc)
    fp.close()

def startup(proj):
    cmd = "putup -p %s %s " % (proj,proj)
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
    mc = open(sphinx_conf).read()
    template =  Template(mc)
    main = template.render(projName=proj)
    mainpy = "%s/docs/conf.py" % (proj)
    fp = open(mainpy,"w")
    fp.write(main)
    fp.close()

    # add config.py
    cmd = "cp %s %s/%s" % (config,proj,proj)
    os.system(cmd)

    #4. bin
    cmd = "mkdir -p %s/bin" % proj
    os.system(cmd)

    # bin/project.py    
    mc = open(raw).read()
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

    mc = open(arrange).read()
    template = Template(mc)
    md = template.render(projName=proj)
    mdocker = "%s/%s/arranger/arrange.py" % (proj,proj)
    fp = open(mdocker,"w")
    fp.write(md)
    fp.close()

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
    os.chdir("tests")
    os.system("mkdir -p data")
    os.system("touch data/arrange.yml")
    os.system("touch data/report.yml")
    os.system("touch data/main.yml")
   
    arrange_templ = os.path.join(sdir,"test_arrange.py") 
    render(arrange_templ,"test_arrange.py",proj)
    report_templ = os.path.join(sdir,"test_report.py")
    render(report_templ,"test_report.py",proj)
    main_templ = os.path.join(sdir,"test_main.py")
    render(main_templ,"test_main.py",proj)
    os.chdir(curdir)
    os.chdir(proj)
    os.chdir("docs")
    index_templ = os.path.join(sdir,"index.rst")
    render(index_templ,"index.rst",proj)

    

    os.chdir(curdir)
    report_templ = os.path.join(sdir,"template.md")
    home = os.environ["HOME"]
    tdir = os.path.join(home,".templates")
    os.system("mkdir -p %s" % tdir)
    md = "%s_template.md" % proj
    report_md = os.path.join(tdir,md)
    render(report_templ,report_md,proj)
    os.system("ln -s %s %s/%s/reporter/" % (report_md,proj,proj))
    
    os.chdir(proj)
    os.system("git add . -A") 
    os.system("git commit -m 'init my project'") 
    #8. git remote add  
    os.system("git remote add origin git@123.57.226.13:/expan/DevRepos/%s.git"%proj)
    
if __name__ == "__main__":
    import sys
    startup(sys.argv[1]) 
