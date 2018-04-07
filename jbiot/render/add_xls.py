import xlrd
import os

def checkexists(afile):
    if os.path.exists(afile):
        return 1

def render_xls(xls):
    data = xlrd.open_workbook(xls)
    table = data.sheets()[0]
    nr = table.nrows
    nc = table.ncols

    # add header
    tab = ""
    head_items = table.row_values(0) 
    head_line = "|" + "|".join([str(it) for it in head_items]) + "|" + "\n"
    tab = tab + head_line
    
    align = []
    for i in range(nc):
        align.append("-")
    line = "|" + "|".join(align) + "|\n"
    tab = tab + line
    if nr == 1:
        return tab
    row_num = 10
    if nr < 10: row_num = nr
    for i in range(1,row_num):
        cont_items = table.row_values(i)
        cont_line = "|" + "|".join([str(it) for it in cont_items]) + "|" + "\n"
        tab = tab + cont_line
    tab = tab + "\n"
    return tab

def add_xls(table):
    if not table:
        return "no table data"
    if type(table) == str and checkexists(table):
        tab = render_xls(table)
        return tab

    if type(table) == list and checkexists(table[0]):
        tab = render_xls(table[0]) 
        return tab

    if type(table) == dict:
            v = table.values()
            if checkexists(v[0]):
                tab = render_xls(v[0])
                return tab
    return "no table data"
