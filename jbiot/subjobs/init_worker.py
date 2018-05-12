import os
import re
import signal
import sys

pid_pat =  re.compile("\((\d+?)\)") 

def init_worker(parent_id):
    print parent_id
    def sig_init2(signal_num,frame):
        cmd = "pstree -p %s" % parent_id
        p = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        out = p.stdout.read()
        pids = pid_pat.findall(out)
        pids = set(pids)
        print pids
        for pid in pids:
            cmd = "kill -9 %s 1>>/dev/null 2>>/dev/null"  % pid
            os.system(cmd)
        cmd = "kill -9 %s 1>>/dev/null 2>>/dev/null" % parent_id
        os.system(cmd)

        pid = os.getpid()
        cmd = "kill -9 %s 1>>/dev/null 2>>/dev/null" % pid
        os.system(cmd)
        sys.exit()
    '''
    def sig_int(signal_num, frame):
        parent = psutil.Process(parent_id)
        for child in parent.children():
            if child.pid != os.getpid():
                child.kill()
        parent.kill()
        psutil.Process(os.getpid()).kill()
    '''
    signal.signal(signal.SIGINT, sig_init2)

