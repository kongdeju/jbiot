
import sys

sys.path.append("../jbiot")
from subjobs.lsub import lsub

cmd = "data/test.cmd"
cmd2 = "data/test2.cmd"


def test_lsub():
    lsub(cmd,0)
    lsub(cmd2,0)


if __name__ == "__main__":
    test_lsub()
