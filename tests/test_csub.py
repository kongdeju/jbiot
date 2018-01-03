import sys
sys.path.append("../")

from jbiot import csub

cmd = "data/lsub.cmd"

def test_lsub():
    csub(cmd,2)

