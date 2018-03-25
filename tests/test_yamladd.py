import sys
sys.path.append("../jbiot")

from yamladd import yamladd


yml = "data/test.yml"

adict = {"fastqInfo":"test.xls"}


print yamladd(yml,adict)






