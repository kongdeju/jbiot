#!/usr/bin/env python
import os

def docker2sing(dimg):
    cmd = "docker run -v /var/run/docker.sock:/var/run/docker.sock -v ${PWD}:/output --privileged -t --rm singularityware/docker2singularity %s" % dimg
    os.system(cmd)

if __name__ == "__main__":
    from docopt import docopt
    usage = """
    Usage:
      docker2sing.py <dockerImg>

    Options:
      -h,--help     print this screen
      dockerImg     docker image from dockerhub or local server
    """
    args = docopt(usage)
    dimg = args["<dockerImg>"]
    docker2sing(dimg)

