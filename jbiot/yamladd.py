import yaml

def yamladd(yml,dict2):
    fp = open(yml)
    ystr = fp.read()
    fp.close()

    fp = open(yml,"w")
   
    fp.write(ystr)
   
    if dict2: 
        ystr = yaml.dump(dict2,default_flow_style=False)
        fp.write(ystr)
    fp.close()
    out = {}
    out["yaml"] = yml 
    return out


    
