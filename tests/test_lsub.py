import sys
sys.path.append("../")

from jbiot import lsub

cmd = "data/lsub.cmd"

def test_lsub():
    lsub(cmd,2)

