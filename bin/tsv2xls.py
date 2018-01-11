#!/usr/bin/env python
#coding=utf-8
import xlwt

def tsv2xls(tsv):
    
    prex = tsv.rsplit(".",1)[0]
    xlsfile = prex + ".xls"
    workbook = xlwt.Workbook()
    sheet1=workbook.add_sheet('sheet1',cell_overwrite_ok=True)

    fp = open(tsv)
    lines = fp.readlines()
    for i in range(len(lines)):
        items = lines[i].strip("\n").split("\t")
        for j in range(len(items)):
            sheet1.write(i,j,items[j])

    workbook.save(xlsfile)



if __name__ == "__main__":
    import sys
    tsv2xls(sys.argv[1])
    
        
