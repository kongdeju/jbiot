import os

def checkexists(afile):
    if os.path.exists(afile):
        return 1



def handle_pngs(pngs):
    
    if type(pngs) == dict:
        pngs = pngs.values()

    reals = []
    for png in pngs[:5]:
        if checkexists(png):
            reals.append(png)
    return reals
