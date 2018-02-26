from JYTools.JYWorker import RedisWorker


class jbiotWorker(RedisWorker):

    def execMyfunc(self,myfunc,params):
        output = myfunc(params)
        cmds = ["sh","run.cmd"]
        self.execute_subprocess(cmds)
        for k,v in output.items():
            self.set_output(k,v)



