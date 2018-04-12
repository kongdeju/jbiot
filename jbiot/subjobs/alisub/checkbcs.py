import os
def checkbcs():
    home = os.environ["HOME"]
    cfg = ".batchcompute/cliconfig"
    cfg = os.path.join(home,cfg)
    if not os.path.exists(cfg) : 
        return 
    lines = open(cfg).readlines()
    if len(lines) >= 7:
        return 1

  
    

