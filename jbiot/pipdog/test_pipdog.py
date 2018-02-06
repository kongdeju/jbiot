import time
from pipdog import pipdog as pd

def task1(params):
    time.sleep(2)
    print "executing task1..."
    print "getinput %s" % params["input"]
    return 1 

def task2(params):
    time.sleep(2)
    inp = params["input"]
    print "executing task2..."
    print "getinput %s" % params["input"]
    return 2

def task3(params):
    time.sleep(1)
    print "executing task3..."
    print "getinput %s" % params["input"]
    return 3

def task4(params):
    time.sleep(1)
    print "executing task4..."
    print "getinput %s" % params["input"]
    return 4

params = {"input":["a","b","c"]}

pipdef = [ {task1} , { task2 } , [task4]  ]

pip = pd(pipdef,params)
pip.run()

print pip.curout

