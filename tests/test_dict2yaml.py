import sys
sys.path.append("../jbiot")

from dict2yaml import dict2yaml


yml = "data/test.yml"

adict = {"fastqInfo":"test.xls"}


print dict2yaml(yml,adict)






