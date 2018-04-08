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
    osspath = os.path.join(osspath,relobj)
    bucket = oss2.Bucket(auth,region,buc)
    objs = []
    for obj in oss2.ObjectIterator(bucket,osspath):
        ossobj = "oss://%s/%s" % (buc,obj.key)
        objs.append(ossobj)
    return objs
#print osslist("oss://jbiobio/working","")    

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


