#!/usr/bin/env python
#coding=utf-8

import sys
import os
dirpath = os.path.join(os.path.dirname(os.path.abspath(__file__)),"../")
sys.path.insert(0,dirpath)
from jbiot.jbio.jmail import jmail

if __name__ == "__main__":
    from docopt import docopt
    usage="""
    Usage:
        jmail.py -t <email> -s <subject> -c <content> 

    jmail is used to auto send email to user 

    Options:
        -t,--to=<email>             target email
        -s,--subject=<subject>      subject of the email
        -c,--content=<content>      content of the email
    
    """

    args = docopt(usage)
    to = args["--to"]
    sub = args["--subject"]
    cont = args["--content"]
    jmail(to,sub,cont)





