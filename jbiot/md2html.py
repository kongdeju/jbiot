#!/usr/bin/env python
import os

mkdoctmplate = "/lustre/users/kongdeju/mkdocsTemplate"
mkdocs = "mkdocs"

def md2html(md):
    curdir = os.getcwd()

    cmd = "cp -r %s mkdocFiles" % mkdoctmplate
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


if __name__ == "__main__":

    from docopt import docopt

    usage = """
    Usage:
        md2html.py <md>

    Options:
       -h --help     just print this screen
       mdfile        markdown format file
       output        default is html directory. and also html.tgz
    """
    args = docopt(usage)

    md = args["<md>"]
    md2html(md)


