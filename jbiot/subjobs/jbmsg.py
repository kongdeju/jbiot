import os
import yaml
from jblog import readlog
from cmd2showdoc import cmd2showdoc
from ..jbio.jmail import jmail
def reademail():
    home = os.environ["HOME"]
    cfg = os.path.join(home,".lcsub","config.yml")
    if not os.path.exists(cfg):
        return

    fp = open(cfg)
    cfg = yaml.load(fp.read())
    if not cfg:
        return
    if "email" in cfg:
        return cfg["email"]

def setemail(email):
    home = os.environ["HOME"]
    cfg = os.path.join(home,".lcsub","config.yml")
    cfgdir = os.path.join(home,".lcsub")
    if not os.path.exists(cfgdir):
        os.mkdir(cfgdir)
    if os.path.exists(cfg):
        infodict = yaml.load(open(cfg).read())
    if not infodict:
        infodict = {}
    infodict["email"]  = email
    fp = open(cfg,"w")
    outstr = yaml.dump(infodict,default_flow_style=False)
    fp.write(outstr)

def readwechat():
    home = os.environ["HOME"]
    cfg = os.path.join(home,".lcsub","config.yml")
    if not os.path.exists(cfg):
        return

    fp = open(cfg)
    cfg = yaml.load(fp.read())
    if not cfg:
        return
    if "wechat" in cfg:
        return cfg["wechat"]

def setwechat(wechat):
    home = os.environ["HOME"]
    cfg = os.path.join(home,".lcsub","config.yml")
    cfgdir = os.path.join(home,".lcsub")
    if not os.path.exists(cfgdir):
        os.mkdir(cfgdir)
    if os.path.exists(cfg):
        infodict = yaml.load(open(cfg).read())
    if not infodict:
        infodict = {}
    infodict["wechat"]  = wechat

    fp = open(cfg,"w")
    outstr = yaml.dump(infodict,default_flow_style=False)
    fp.write(outstr)


def jbmsg(cmdfile,email,name):
    
    body = readlog()
    if email:
        setemail(email)

    email = reademail()
    if email and name:
        jmail(email,name,body)

    if name:
        cmd2showdoc(name,cmdfile)













