#!/usr/bin/env python
#coding=utf-8
import xlrd

def xls2tsv(xls):
    
    prex = xls.rsplit(".",1)[0]
    tsvfile  = prex + ".tsv"
    workbook = xlrd.open_workbook(xls)
    table = workbook.sheets()[0]
    nrows = table.nrows

    fp = open(tsvfile,"w")    
    for i in xrange(0,nrows):
        rowValues = table.row_values(i)
        line = "\t".join(rowValues) + "\n"
        fp.write(line)
    fp.close()

    return tsvfile

if __name__ == "__main__":
    from docopt import docopt
    usage = """
    Usage:
        xls2tsv.py <xls>
        
    Options:
        -h --help  print this screen
        <xls>      excel file .xls

    """
    args = docopt(usage)
    xls = args["<xls>"]
    tsv2xls(xls)
    
