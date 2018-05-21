#!/usr/bin/env python
import sys
from collections import OrderedDict
def getsamecols(tabs,sep=" "):
    heads = []
    for tab in tabs:
        fp = open(tab)
        headline = fp.readline()
        items = headline.strip().split(sep)
        heads.append(items)
    samecols = heads[0]
    for i in range(1,len(heads)):
        samecols = set(samecols) & set(heads[i])
    
    cols = []
    for col in samecols:
        idx = heads[0].index(col)
        cols.append([col,idx])
    cols = sorted(cols,key=lambda x: x[1])
    
    cols = [ item[0] for item in cols]    
    return cols

def getallcols(tabs,sep):
    totalcols = []
    heads = []
    for tab in tabs:
        fp = open(tab)
        headline = fp.readline()
        items = headline.strip().split(sep)
        for item in items:
            if item in totalcols:
                pass
            else:
                totalcols.append(item)
    return totalcols

def gettabkeys(tdicts,mode):
    tabkeys = set(tdicts[tdicts.keys()[0]].keys())
    for tabname in tdicts.keys()[1:]:
        tdict = tdicts[tabname]
        tkeys = set(tdict.keys())
        if mode == "intersect":
            tabkeys = tabkeys & tkeys
        else:
            tabkeys = tabkeys | tkeys

    return tabkeys


def tab2dict(tab,cols,sep=" "):
    fp = open(tab)
    headline = fp.readline()
    heads = headline.strip().split(sep)
    idxes = []
    tdict = {}
    for col in cols:
        idx = heads.index(col)
        idxes.append(idx)
    for line in fp.readlines():
        items = line.strip().split(sep)
        ks = []
        for i in idxes:
            ks.append(items[i])
        vs = []
        for i in range(len(items)):
            if i in idxes:
                continue
            vs.append(items[i])
        k = sep.join(ks)
        tdict[k]  = vs
    return tdict


def jointabdicts(tabdicts,tabkeys):
    
    samples = tabdicts.keys()

    tabvals = {}
    for sample,tdict in tabdicts.items():
        svalues = tdict[tdict.keys()[0]]
        num_vals = len(svalues)
        tabvals[sample] = num_vals


    alls = OrderedDict()
    for tkey in tabkeys:
        items = []
        for sample in samples:
            num_vals = tabvals[sample]
            its = ["."] * num_vals
            if tkey in tabdicts[sample]:
                its = tabdicts[sample][tkey]
            items.extend(its)

        alls[tkey] = items
    return alls

def mergeTable(tabs,samecols=[],mode="intersect",sep=" ",outfile="merge.out"):
    """Merge Tsv files with same column as key.

    """
    # get same tab cols
    allcols = getallcols(tabs,sep)
    if not samecols: 
        samecols = getsamecols(tabs,sep)
    if not samecols:
        sys.stderr.write("no same column !\n ")
        sys.exit()
    # covert tab to dict
    tabdicts = OrderedDict()
    for i in range(len(tabs)):
        tdict = tab2dict(tabs[i],samecols,sep)
        tabdicts[i] =  tdict

    # get tab keys
    tabkeys = gettabkeys(tabdicts,mode)

    # merge them
    allitems = jointabdicts(tabdicts,tabkeys)
    
    # writ to file
    fp = open(outfile,"w")
    headline = sep.join(allcols) + "\n"
    fp.write(headline)
    for k,items in allitems.items():
        ks = k.split(sep)
        ks.extend(items)
        line = sep.join(ks) + "\n"
        fp.write(line)
    fp.close()

    return outfile
    
if __name__ == "__main__":
    from docopt import docopt
    usage = """
    Usage:
        MergeTable.py [options] <tab1,tab2,.>

    Summary:
        MergeTable is designed to merge tables with same columns.

    Options:
        tabs                     tabfile string comma seperated
        -s,--sep=<sep>           seperator [default: \t]
        -m,--mode=<mode>         merge mode intersect | join [default: intersect]
        -c,--cols=<cols>         merge tables in such cols, comma seperated defualt auto-detected
        -o,--out=<outfile>       outfile name [default: merge.out]

    """

    args = docopt(usage)  
    sep = args["--sep"] 
    mode = args["--mode"]
    cols = args["--cols"]
    if cols:
        cols = cols.split(",")
    out = args["--out"]
    tabs = args["<tab1,tab2,.>"].split(",")
    mergeTable(tabs,cols,mode,sep,out)


