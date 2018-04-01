
import sys
sys.path.insert(0,"../jbiot")

from subjobs.stripcmd import stripcmd


cmdfile = "data/test.cmd"

def test_stripcmd():

    stripcmd(cmdfile)


if __name__ == "__main__":
    test_stripcmd()
