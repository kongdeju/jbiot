import sys
sys.path.append("../jbiot")
from subjobs.csub.csub import csub

cmdfile = "data/test.cmd"

def test_csub():
    csub(cmdfile,False,False,False,False)

if __name__ == "__main__":
    test_csub()
