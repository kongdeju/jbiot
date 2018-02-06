import yaml

class pipdog():

    def __init__(self,pipdef,params):
        """init pipdog class
        Args:
            tasks (func) :  worker
            params (dict) : params,keys are pip_tasks,pip_input,pip_output

        Returns:
            object

        """

        self.pipdef = pipdef
        self.params = params
        self.params["output"] = {}

    def run(self):
        tasks = []
        items = self.pipdef
        for task in items:
            tasks.append(task)
            
        for task in tasks:
            # load task params
            if not type(task) == set and not type(task) == list:
                tparams = {}
                taskname = task.__name__

                if taskname in self.params:
                    tparams = self.params[taskname]
                tparams["input"] = self.params["input"]

                out = task(tparams)
                self.params["output"][taskname]  = out

            elif type(task) == set :
                tasks = task
                for task in tasks:
                    task = task
                    tparams = {}
                    taskname = task.__name__
                    if taskname in self.params:
                        tparams = self.params[taskname]
                    tparams["input"] = self.params["input"] 
                    self.params["output"][taskname] = []
                  
                    for inp in tparams["input"]:
                        tparams["input"] = inp
                        out = task(tparams)
                        self.params["output"][taskname].append(out)
                self.params["input"] = self.params["output"][taskname]

            elif type(task)  == list:
                tasks = task
                for task in tasks:
                    task = task
                    tparams = {}
                    taskname = task.__name__
                    if taskname in self.params:
                        tparams = self.params[taskname]
                    tparams["input"] = self.params["input"]
                    self.params["output"][taskname] = []

                    out = task(tparams)
                    self.params["output"][taskname].append(out)
                self.params["input"] = self.params["output"][taskname]


    @property
    def curout(self):
        return self.params["output"]

    @property
    def curin(self):
        return self.params["input"]


    def runTask(self):
        pass

    def runTasks(self):
        pass
