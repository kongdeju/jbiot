#!/usr/bin/env python
#coding=utf-8
import os
import gzip
import json
import yaml

usage = """

Usage:
  smartFq.py -d <dir> [-o <json>] [-f <fmt>] [--rel]

Options:
  -d <dir> --dir <dir>        fastq directory,prefer absolute path 
  -o <json> --out <json>      output json file 
  -f <yaml> --yaml <yaml>     output yaml
  --rel                       use relative path [default: False]
        """

def testFq(fq):
    fp = open(fq)
    fqid = fp.readline()
    fqseq = fp.readline()
    flag = fp.readline()
    score = fp.readline()
    if fqid.startswith("@") and flag == "+":
        return 1
    

def smartFqs(indir,out,yml,rel):
    fqs = []
    pair = {}
    curdir = os.getcwd() 
    for root,dirs,files in os.walk(indir):
        for file in sorted(files):
            absfile = os.path.join(curdir,root,file)
            if rel:
                absfile = os.path.join(root,file)
            if file.find("fq") != -1 or file.find("fastq") != -1 and testFq(absfile) :
                # smart fq
                #absfile = os.path.join(root,file)
                prex = absfile.split("/")[-1] 
                prex = prex.rstrip(".fq") 
                prex = prex.rstrip(".fastq") 
                prex = prex.rstrip(".fq.gz")
                prex = prex.rstrip(".fastq.gz")
                fqs.append([absfile,prex])
               
                fp = open(absfile) 
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
    
    outdict = {"fastqs":outdict,"groups":None}
    jstr = json.dumps(outdict)
    ystr = yaml.dump(outdict,default_flow_style=False)  
    print ystr
    if out :
        fp = open(out,"w")
        fp.write(jstr)
        fp.close()

    if yml:
        fp = open(yml,"w") 
        fp.write(ystr)
        fp.close()


if __name__ == "__main__":
    import docopt
    args = docopt.docopt(usage)
    indir = args["--dir"]
    prex = args["--out"]
    fmt  = args["--yaml"]
    rel = args["--rel"]
    smartFqs(indir,prex,fmt,rel)

