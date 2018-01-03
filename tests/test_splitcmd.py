import sys
sys.path.append("../")

from jbiot import splitcmd

cmd = "data/test.cmd"
cmd2 = "data/test2.cmd"

def test_splitcmd():
    splitcmd(cmd)
    #splitcmd(cmd2)


