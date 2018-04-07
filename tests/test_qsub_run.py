import sys
sys.path.insert(0,"../")
from jbiot.subjobs.csub.qsub_run import qsub_run


cmd = "ls -lht"

def test_qsub_run():
    
    print qsub_run("abcsf","2G",cmd)


if __name__ == "__main__":
    test_qsub_run()



