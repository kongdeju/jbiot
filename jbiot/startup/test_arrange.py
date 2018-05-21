import sys

sys.path.append("../")

from {{projName}}.arranger.arrange import arrange

ymlfile = "data/arrange.yml"

def test_arrange():
    arrange(ymlfile)



if __name__ == "__main__":
    test_arrange()



