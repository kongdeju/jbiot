from base64 import b64encode
from PIL import Image

def b64(afile):
    fp = open(afile)
    c = b64encode(fp.read())
    return c


print b64("test.svg")
