from JYTools.JYWorker import RedisWorker
import os

class jbiotWorker(RedisWorker):

    def execMyfunc(self,myfunc,params):
        output = myfunc(params)
        if os.path.exists("run.cmd"):
            cmds = ["sh","run.cmd"]
            self.execute_subprocess(cmds)
        for k,v in output.items():
            self.set_output(k,v)



