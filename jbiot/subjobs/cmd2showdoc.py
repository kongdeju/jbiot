#!/usr/bin/env python
#coding=utf-8
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
import requests
import json
import os
import getpass
import time
host = "http://jbio.cc:5525/"

def cmd2showdoc(pageName,cmdFile):
    user = getpass.getuser()
    ftime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())) 
    pageCont = '''
`%s`
`%s`

    ''' % (user,ftime)

    fp = open(cmdFile)
    cmdCont = fp.read()

    pageCont = pageCont + cmdCont
    data = { 
        "api_key" : "13f5a8025ccbe460b1f12ee709ca6d121829804879",
        "api_token" :  "ded06d51d54ca9075d693a60f5f1003b784221269",
        "page_title" :  pageName,
        "page_content" : pageCont ,
        "cat_name": "项目工作",
        "cat_name_sub" : "操作命令"
    }
    url = host + "/server/index.php?s=/api/item/updateByApi"
    #url = "http://www.genescret.com:5525/server/api/item/updateByApi"
    req = requests.post(url,data=data)

