#!/usr/bin/env python
import os

dirpath = os.path.dirname(os.path.abspath(__file__))
mkdoctemplate = os.path.join(dirpath,"mkdocsTemplate.tgz")
mkdocs = "mkdocs"

def get_style(style):
    home = os.environ["HOME"]
    mdir = os.path.join(home,".mkdocstyles")
    if not os.path.exists(mdir):
        os.mkdir(mdir)
    tgz = style + ".tgz"
    tgz = os.path.join(mdir,tgz)
    if os.path.exists(tgz):
        return tgz
    url = "www.genescret.com:6636/dev-report/styles/%s.tgz" % style
    cmd = "wget -P %s %s" % (mdir,url)
    os.system(cmd)
    return tgz

def md2html(md,style):
    mkdoctemplate = get_style(style)

    curdir = os.getcwd()
    cmd = "tar xvzf %s" % mkdoctemplate
    os.system(cmd)
    
    mkdocsdir = mkdoctemplate.split("/")[-1].split(".")[0]
    cmd = "cp -r %s mkdocFiles" % mkdocsdir
    os.system(cmd)

    cmd = "rm -rf %s" %  mkdocsdir
    os.system(cmd)

    cmd = "cp %s mkdocFiles/docs/index.md" % md
    os.system(cmd)

    os.chdir("mkdocFiles")

    cmd = "mkdocs build"
    os.system(cmd)

    os.chdir(curdir)

    cmd = "cp -r mkdocFiles/site html"
    os.system(cmd)
    cmd = "rm -rf mkdocFiles"
    os.system(cmd)

    cmd = "tar cvzf html.tgz html/"
    os.system(cmd)

    cmd = "rm -rf html/"
    os.system(cmd)


if __name__ == "__main__":

    from docopt import docopt

    usage = """
    Usage:
        md2html.py <md> [ -s <style> ] 
    
    md2html.py is designed to transfer markdown file to html file 
    using mkdocs to build this process.

    Options:
       -h --help            just print this screen
       <md>                 markdown format file
       -s,--style=<style>   mkdoc templates in tgz format,[default: mkdocsTemplate] 
       output               default ouput html.tgz
    """
    args = docopt(usage)
    md = args["<md>"]
    style = args["--style"]
    md2html(md,style)

