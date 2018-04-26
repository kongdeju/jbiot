import sys

sys.path.append("../")

from {{projName}}.arranger.arrange import arrange

indict = {"yaml":"data/arrange.yml"}

def test_arrange():
    arrange(indict)



if __name__ == "__main__":
    test_arrange()



