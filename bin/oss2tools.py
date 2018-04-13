#!/usr/bin/env python
#coding=utf-8
import sys
import os
dirpath = os.path.join(os.path.dirname(os.path.abspath(__file__)),"../")
sys.path.insert(0,dirpath)
from jbiot.subjobs.alisub.ossio.oss2tools import *


if __name__ == "__main__":
    from docopt import docopt
    usage = """
    Usage:
        oss2tools.py list      <ossdir>
        oss2tools.py mapdown   <ossdir>
        oss2tools.py mapup     <ossdir>
        oss2tools.py download  <ossobj> <localobj>
        oss2tools.py upload    <localobj> <ossobj>
        oss2tools.py reldown   <ossdir> <relobj>
        oss2tools.py relup     <ossdir> <localobj>
        oss2tools.py absdown   <ossobj>   
        oss2tools.py absup     <localobj> 

    Options:
        <ossdir>         ossdir in such format. oss://bucket/dir/
        <relobj>         ossfile in relative path.
        <ossobj>         ossobject.
        <localobj>       local file or directory

    """
    args = docopt(usage)
    mapdownflag = args["mapdown"]
    mapupflag = args["mapup"]
    reldownflag = args["reldown"]
    absdownflag = args["absdown"]
    uploadflag = args["upload"]
    downloadflag = args["download"] 
    relupflag = args["relup"]
    absupflag = args["absup"]
    listflag = args["list"]


    ossdir = args["<ossdir>"]
    relobj = args["<relobj>"]
    ossobj = args["<ossobj>"]
    localobj = args["<localobj>"]

    if mapdownflag:
        mapdown(ossdir)
    if mapupflag:
        mapup(ossdir)
    if reldownflag:
        reldown(ossdir,relobj)
    if absdownflag:
        absdown(ossobj)
    if uploadflag:
        ossupload(localobj,ossobj) 
    if downloadflag:
        ossdownload(ossobj,localobj)   
    if relupflag :
        relup(ossdir,localobj) 
    if listflag :
        print osslist(ossdir,"")

