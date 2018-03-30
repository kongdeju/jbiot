from JYTools.JYWorker import RedisWorker
import os
import yaml

class jbiotWorker(RedisWorker):
    def execMyfunc(self,myfunc,params):
        if "yaml" in params:
            yml = params["yaml"]
        indict = yaml.load(open(yml).read())
        if "work_dir" in indict:
            wdir = indict["work_dir"] 
            if not os.path.exists(wdir): os.mkdir(wdir)
            os.chdir(wdir)
        output = myfunc(params)
        if os.path.exists("run.cmd"):
            cmds = ["sh","run.cmd"]
            self.execute_subprocess(cmds)
        for k,v in output.items():
            self.set_output(k,v)

