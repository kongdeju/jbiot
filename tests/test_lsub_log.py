import sys
sys.path.append("../jbiot")
from subjobs.lsub_log import readlog

def test_readlog():
    readlog("data/test.cmd")

if __name__ == "__main__":
    test_readlog()
