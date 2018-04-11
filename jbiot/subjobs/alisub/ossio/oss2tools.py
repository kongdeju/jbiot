import oss2
import sys
import os
import yaml

def readinfo():
    inf = os.path.join(os.environ["HOME"],".lcsub","config.yml")
    infdict = yaml.load(open(inf).read()) 
    key = infdict["key"] 
    secret = infdict["secret"]
    region = infdict["region"]  
    return key,secret,region
key,secret,region = readinfo()
auth = oss2.Auth(key,secret)


def osslist(ossdir,relobj):
    buc = ossdir[6:].split("/")[0]
    osspath = ossdir[6+len(buc)+1:]
    if relobj:
        osspath = os.path.join(osspath,relobj)
    bucket = oss2.Bucket(auth,region,buc)
    objs = []
    for obj in oss2.ObjectIterator(bucket,osspath):
        ossobj = "oss://%s/%s" % (buc,obj.key)
        objs.append(ossobj)
    return objs
#print osslist("oss://jbiobio/working/oss2tools.py","")    
#print osslist("oss://jbiobio/data/tmp","")

def ossdirmapping(ossdir):
    ossdir = ossdir.rstrip("/")
    buc = ossdir[6:].split("/")[0]
    osspath = ossdir[6+len(buc)+1:]
    bucket = oss2.Bucket(auth,region,buc)
    for obj in oss2.ObjectIterator(bucket,osspath):
        ossdir = obj.key
        localdir = ossdir[len(osspath)+1:]
        if "/" in localdir:
            localdir = localdir.rsplit("/",1)[0]
            cmd = "mkdir -p %s" % localdir
            os.system(cmd)
#ossdirmapping("oss://jbiobio/working/")

def ossupload(localfile,ossdir):
    buc = ossdir[6:].split("/")[0]
    osspath = ossdir[6+len(buc)+1:]
    buc = oss2.Bucket(auth,region,buc)
    if not os.path.exists(localfile):
        return

    if not os.path.isdir(localfile):
        osspath = os.path.join(osspath,localfile)
        res = buc.put_object_from_file(osspath,localfile)
        if res.status == 200:
            msg = "Upload %s to %s successfully" % (localfile,osspath)
    else:
        for root,dirs,files in os.walk(localfile) :
            for f in files:
                absfile = os.path.join(root,f)
                osspath2 = os.path.join(osspath,absfile)
                res = buc.put_object_from_file(osspath2,absfile)
                if res.status == 200:
                    msg = "Upload %s to %s successfully" % (localfile,osspath2)

#ossupload("em","oss://jbiobio/working/")
def ossdownload(ossdir,obj):
    buc = ossdir[6:].split("/")[0]
    Buc = oss2.Bucket(auth,region,buc)
    objs = osslist(ossdir,obj) 
    for oj in objs:
        if oj.endswith("/"):
            continue
        localfile = oj[len(ossdir)+1:]
        if "/" in localfile:
            localdir = localfile.rsplit("/",1)[0]
            cmd = "mkdir -p %s" % localdir
            os.system(cmd)
        osspath = oj[6+len(buc)+1:]
        res = Buc.get_object_to_file(osspath,localfile)
        if res.status == 200:
            msg = "Download %s to %s successfully" % (oj,localfile)
#ossdownload("oss://jbiobio/working","em")

def ossprofile(ossdir):
    buc = ossdir[6:].split("/")[0]
    osspath = ossdir[6+len(buc)+1:]
    bucket = oss2.Bucket(auth,region,buc)
    profile = {}
    for obj in oss2.ObjectIterator(bucket,osspath):
        name = obj.key
        name = name[len(osspath)+1:]
        if  name.endswith("/"):
            continue
        if not name:
            continue
        size = obj.size
        profile[name] = size
    return profile

#print ossprofile("oss://jbiobio/working")

def localprofile():
    profile = {}
    for root,dirs,files in os.walk("."):
        for f in files:
            absfile = os.path.join(root,f)
            size = os.path.getsize(absfile)
            profile[absfile[2:]] = size
    return profile

#print localprofile()


def checkdiff(ossdir):
    ossprf = ossprofile(ossdir)
    lclprf = localprofile()
    
    touploads = []
    for ln,lz in lclprf.items():
        if ln in ossprf and lz == ossprf[ln]:
            continue
        touploads.append(ln)
    return touploads

#checkdiff("oss://jbiobio/working")

def mapdown(ossdir):
    ossdirmapping(ossdir)


def mapup(ossdir):
    touploads = checkdiff(ossdir)
    for lf in touploads:
        ossupload(lf,ossdir)
  
def reldown(ossdir,relfile):
    ossdownload(ossdir,relfile)

def absdown(ossobj):
    buc = ossobj[6:].split("/")[0]
    Buc = oss2.Bucket(auth,region,buc)
    objs = osslist(ossobj,"")
    for obj in objs:
        if obj.endswith("/"):
            continue
        osspath = obj[6+len(buc)+1:]
        localfile = os.path.join("/tmp",buc,osspath)
        localdir = localfile.rsplit("/",1)[0]
        os.system("mkdir -p %s" % localdir)
        res = Buc.get_object_to_file(osspath,localfile)

if __name__ == "__mains__":
    from docopt import docopt

    usage = """

    Usage:
        oss2tools.py mapdown   <ossdir>
        oss2tools.py mapup     <ossdir>
        oss2tools.py reldown   <ossdir> <relobj>
        oss2tools.py absdown   <ossobj>    
        oss2tools.py upload    <localobj> <ossobj>
        oss2tools.py download  <ossobj> <localobj>

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
    ossdir = args["<ossdir>"]
    relobj = args["<relobj>"]
    absobj = args["<ossobj>"]

    if mapdownflag:
        mapdown(ossdir)
    if mapupflag:
        mapup(ossdir)
    if reldownflag:
        reldown(ossdir,relobj)
    if absdownflag:
        absdown(absobj)

