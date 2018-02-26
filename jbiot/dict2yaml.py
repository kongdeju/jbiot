import yaml

def dict2yaml(dic):
    config  = "conf.yaml"
    fp = open(config)
    ystr = yaml.dump(dic)
    fp.write(ystr)
    fp.close()
    return config


    
