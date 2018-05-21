import os

def test_main():

    cmd = "../bin/{{projName}}.py -c data/main.yml"
    os.system(cmd)


if __name__ == "__main__":
    test_main()
