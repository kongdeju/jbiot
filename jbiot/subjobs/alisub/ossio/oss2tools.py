import  oss2
import sys
import os
import yaml

def readinfo():
    #inf = os.path.join(os.environ["HOME"],".lcsub","config.yml")
    #infdict = yaml.load(open(inf).read()) 
    key = "QFmrMPB18qNx9KYc"
    secret = "IuAdh4qL9noDf0UnMOO977HSgZSc0E"
    region = "oss-cn-beijing.aliyuncs.com"
    try:
        region = os.environ["BATCH_COMPUTE_OSS_HOST"]
    except:
        pass
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
#print osslist("oss://jbiobio/data/tmp/tmp","")

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

        osstest = ossdir.rstrip("/")
        objs = osslist(ossdir,"")
        objs2 = osslist(ossdir+"/","")
        
        if ( objs and objs2) or ossdir.endswith("/") :
            osspath = os.path.join(osspath,localfile.split("/")[-1])
        else:
            osspath = os.path.join(osspath)
        res = buc.put_object_from_file(osspath,localfile)
    else:
        localfile = localfile.rstrip("/")
        osstest = ossdir.rstrip("/")
        objs = osslist(ossdir,"")
        objs2 = osslist(ossdir+"/","")
        if ( objs and objs2 ) or ossdir.endswith("/"):
            dirname = localfile.rstrip("/").split("/")[-1]
            for root,dirs,files in os.walk(localfile) :
                for f in files:
                    absfile = os.path.join(root,f)
                    relpath = absfile[len(localfile)+1:]
                    osspath2 = os.path.join(osspath,dirname,relpath)
                    res = buc.put_object_from_file(osspath2,absfile)
        else:
            for root,dirs,files in os.walk(localfile) :
                for f in files:
                    absfile = os.path.join(root,f)
                    relpath = absfile[len(localfile)+1:]
                    osspath2 = os.path.join(osspath,relpath)
                    #print absfile,osspath2
                    res = buc.put_object_from_file(osspath2,absfile)



#ossupload("em","oss://jbiobio/working/")
#ossupload("oss2tools.py","oss://jbiobio/working/oss2tools.py")
def ossdownload(ossdir,lf):

    buc = ossdir[6:].split("/")[0]
    Buc = oss2.Bucket(auth,region,buc)
    objs = osslist(ossdir,"")
    if not objs:
        return

    #ossobj is a file
    if len(objs) == 1 and ( not objs[0].endswith("/")):
        osspath = objs[0][6+len(buc)+1:]
       
        if lf.endswith("/"):
            os.system("mkdir -p %s" % lf)
        # lf is dir
        if os.path.isdir(lf) :
            filename = osspath.split("/")[-1]
            localfile = os.path.join(lf,filename)
            res = Buc.get_object_to_file(osspath,localfile)
        # lf is file
        else:
            localfile = lf
            res = Buc.get_object_to_file(osspath,localfile)

    # ossobj is a dir
    else:
        if lf == "." or lf == ".." or lf == "~" or lf == "./" or lf == "../" or lf == "~/":
            dirname= ossdir.strip("/").rsplit("/",1)[-1].strip("/")
            lf = os.path.join(lf,dirname)
        for oj in objs:
            osspath = oj[6+len(buc)+1:]
            ossdir = ossdir.strip("/")
            relpath = oj[len(ossdir)+1:]
            localfile = os.path.join(lf,relpath)
            ldir = localfile.rsplit("/",1)[0]
            if relpath.endswith("/"):
                os.system("mkdir -p %s" % ldir)
                continue
            if not relpath :
                continue
            os.system("mkdir -p %s" % ldir)
            res = Buc.get_object_to_file(osspath,localfile)


#ossdownload("oss://jbiobio/working/group1","test.py")
#ossdownload("oss://jbiobio/working/group1",".")
#ossdownload("oss://jbiobio/working/test","abc")

def ossdownload2(ossdir,obj):
    ossdir = ossdir.rstrip("/") + "/"
    buc = ossdir[6:].split("/")[0]
    Buc = oss2.Bucket(auth,region,buc)
    objs = osslist(ossdir,obj) 
    for oj in objs:
        if oj.endswith("/"):
            continue
        localfile = oj[len(ossdir):]
        if "/" in localfile:
            localdir = localfile.rsplit("/",1)[0]
            cmd = "mkdir -p %s" % localdir
            os.system(cmd)
        osspath = oj[6+len(buc)+1:]
        res = Buc.get_object_to_file(osspath,localfile)

def ossprofile(ossdir):
    buc = ossdir[6:].split("/")[0]
    osspath = ossdir[6+len(buc)+1:].strip("/")
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
        for di in dirs:
            absdir = os.path.join(root,di)
            absdir = absdir[2:]
            if not os.listdir(absdir):
                cmd = "touch %s/.thiswasaemptydirectory" % absdir
                os.system(cmd)
                absfile = os.path.join(absdir,".thiswasaemptydirectory")
                profile[absfile] = 0
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
    ossdir = ossdir.rstrip("/")
    ossdir = ossdir + "/"
    touploads = checkdiff(ossdir)
    for lf in touploads:
        osspath = os.path.join(ossdir,lf)
        ossupload(lf,osspath)

#mapup("oss://jbiobio/working")
  
def reldown(ossdir,relfile):
    ossdownload2(ossdir,relfile)

def relup(ossdir,localfile):
    if not os.path.exists(localfile):
        return
    if os.path.isdir(localfile):
        for root,dirs,files in os.walk(localfile):
            for f in files:
                absf = os.path.join(root,f)
                ossupload(absf,ossdir)
        for di in dirs:
            absdir = os.path.join(root,di)
            if not os.listdir(absdir):
                cmd = "touch %s/.isadirectory" % absdir
            absfile = os.path.join(absdir,".isadirectory")
            ossupload(absfile,ossdir)

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

