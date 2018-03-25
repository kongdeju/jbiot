import yaml

def yamladd(yml,dict2):
    fp = open(yml)
    ystr = fp.read()
    fp.close()
    dict1 = yaml.load(ystr)

    mdict = dict(dict1,**dict2)
    ystr = yaml.dump(mdict,default_flow_style=False)
    fp = open(yml,"w")
   
    fp.write(ystr)
    fp.close()
    out = {}
    out["yaml"] = yml 
    return out


    
