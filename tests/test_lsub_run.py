import sys
sys.path.append("../jbiot")
from subjobs.lsub_run import main


cmd1 = "data/task_01.cmd"
cmd2 = "data/task_02.cmd"

t = 2


def test_main():
    main(cmd1,2)
    main(cmd2,2)


if __name__ == "__main__":
    test_main()
