#coding=utf-8
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
import json
import os

def dict2json(adict,ajson):
    jstr = json.dumps(adict)
    fp = open(ajson,"w")
    fp.write(jstr)
    fp.close()

def json2dict(ajson):
    if not os.path.exists(ajson):
        return {}
    fp = open(ajson)
    adict = json.loads(fp.read())
    return adict

class jsondb(object):
    
    def __init__(self,db):
        self.db = db
    
    def get(self,kname):
        thedict = json2dict(self.db)
        if kname in thedict:
            return thedict[kname]
        return

    def set(self,kname,value):
        thedict = json2dict(self.db)
        thedict[kname] = value
        dict2json(thedict,self.db)

    def add(self,value):
        thedict = json2dict(self.db)
        for i in range(1,10000):
            if str(i) in thedict:
                continue
            i = str(i)
            thedict[i] = value
            dict2json(thedict,self.db)
            return

    def remove(self,kname):
        thedict = json2dict(self.db)
        if kname in thedict:
            thedict.pop(kname)
        dict2json(thedict,self.db)

    def getall(self):
        thedict = json2dict(self.db)
        return thedict

if __name__ == "__main__":

    jd = jsondb("test.json")

    print jd.add("cccd")
    print jd.add("cccd")
    print jd.getall()
