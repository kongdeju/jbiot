#!/usr/bin/env python
#coding=utf-8
import sys
import os

def make_cmd(head_items,filt_str):
    if filt_str == "All":
        filt_cmd = '1'
        return filt_cmd

    filt_items = filt_str.split()
    if not filt_items:
        filt_cmd = '1'
        return filt_cmd
    i = -1
    for item in filt_items:
        i = i + 1
        if item == "==" or item == "!=" :
            key_idx1 = head_items.index(filt_items[i-1])
            filt_items[i-1] = "item%d" % key_idx1
            if filt_items[i+1] == "''":
                filt_items[i+1] = "''"

            else:
                filt_items[i+1] = "'%s'" % filt_items[i+1]
        if item == "has":
            key_idx1 = head_items.index(filt_items[i-1])
            filt_items[i-1] = "'%s'" % filt_items[i+1]
            filt_items[i+1] = "item%d" % key_idx1
            filt_items[i] = "in"
        if item == "in":
            key_idx1 = head_items.index(filt_items[i-1])
            filt_items[i-1] = "item%d" % key_idx1
            filt_items[i+1] = filt_items[i+1].replace("null","")
        if  ">" in item or "<" in item:
            key_idx1 = head_items.index(filt_items[i-1])
            filt_items[i-1] = "Float(item%d)" % key_idx1
            filt_items[i+1] = "%s" % filt_items[i+1]
    filt_cmd = " ".join(filt_items)
    return filt_cmd
            
def Float(str):
    try:
        fnum = float(str)
    except:
        fnum =''
    return fnum

def filt_vars(vas,filt_str):
    head_items = vas[0]
    filt_cmd  = make_cmd(head_items,filt_str)
    filtvars = []
    cmd = "for items in vas[1:]:\n "
    for i in range(len(head_items)):
        cmd = cmd  + "\titem%s = items[%s]\n" % (i,i)
    cmd = cmd + "\tif %s :\n" %  filt_cmd
    cmd = cmd + "\t\tfiltvars.append(items)\n"
    cmd = cmd + "filtvars.insert(0,head_items)"
    #print cmd
    exec(cmd)
    for va in filtvars:
        line = "\t".join(va)
        print line


def main(xls,filt_str):

    vas = []
    fp = open(xls)
    for line in fp:
        items = line.strip("\n").split("\t")
        vas.append(items)
    filt_vars(vas,filt_str)


if __name__ == "__main__":
    import sys
    usage = """
    Usage:
      filtTable.py <table> -f <filter>

    Options:
      -f <filter> --filter=<filter>   filter options like "columnX < 0.9" 
        
    """
    from docopt import docopt
    args = docopt(usage) 

    table = args["<table>"]
    filt = args["--filter"]

    main(table,filt)

