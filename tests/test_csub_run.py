import sys
sys.path.insert(0,"../")
from jbiot.subjobs.csub.csub_run import main


cmdfile = "data/task_01.cmd"

def test_csub_run():
    
    main(cmdfile,"2G",False,False)

if __name__ == "__main__":
    test_csub_run()



