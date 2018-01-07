#!/usr/bin/env python
#coding=utf-8
import os
import gzip
import json

usage = """

Usage:
  smartFq.py -d <dir> [-o <json>]

Options:
  -d <dir> --dir <dir>        fastq directory 
  -o <prefix> --out <prefix>  output prefix of json file default: stdout

        """

def smartFqs(indir,prexfix):
    fqs = []
    pair = {} 
    for root,dirs,files in os.walk(indir):
        for file in sorted(files):
            if file.find("fq") != -1 or file.find("fastq") != -1 :
                # smart fq
                absfile = os.path.join(root,file)
                prex = absfile.split("/")[-1] 
                prex = prex.rstrip(".fq") 
                prex = prex.rstrip(".fastq") 
                prex = prex.rstrip(".fq.gz")
                prex = prex.rstrip(".fastq.gz")
                fqs.append([absfile,prex])
                
                # smart pair
                if file.endswith(".gz"):
                    fp = gzip.open(absfile)
                line  = fp.readline()
                id = line.split()[0].split("/")[0]
                if id in pair:
                    pair[id].append([absfile,prex])
                else:
                    pair[id] = [[absfile,prex]]
    outdict = {}
    for id,items in pair.items():
        
        fqs = []
        prexs = []
        for item in items:       
            fqs.append(item[0])
            prexs.append(item[1])
         
        c = os.path.commonprefix(prexs)
        prex = c.rstrip(".")
        prex = c.rstrip("_r")
        prex = c.rstrip("_R")
        outdict[prex] = items

    out = prex + ".json"
    jstr = json.dumps(outdict,indent=True)

    if prexfix :
        fp = open(out,"w")
        fp.write(jstr)
        fp.close()
    else:
        print jstr

if __name__ == "__main__":
    import docopt
    args = docopt.docopt(usage)
    indir = args["--dir"]
    prex = args["--out"]
    smartFqs(indir,prex)

