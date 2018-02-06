import os

render = "../jbiot/render.py"
tmpl = "data/test.tmpl"
ijson = "data/args.json"
out = "index.md"

def test_render():
    cmd = "python %s -t %s -j %s -o %s" % (render,tmpl,ijson,out)
    print cmd
    os.system(cmd)


if __name__ == "__main__":
    test_render()
