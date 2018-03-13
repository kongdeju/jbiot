#!/usr/bin/env python
#coding=utf-8
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

from wechat_sender import Sender

def send(msg):
    sender = Sender(token="devlab")
    sender.send(msg)


if __name__ == "__main__":
    from docopt import docopt
    usage = """
    Usage:
        jbio.msg <msg>

    Options:
        <msg>      message will send to deju

    """
    args = docopt(usage)
    msg = args["<msg>"]
    send(msg)






