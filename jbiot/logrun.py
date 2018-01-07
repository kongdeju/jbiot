import os

class log:

    @staticmethod
    def run(cmd,prefix="run",run=False,docker=False):

        cmdfile = prefix + ".cmd"
        fp = open(cmdfile,"a")
        cmd = "    %s" % (cmd)
        line = cmd + "\n"
        fp.write(line)

        fp.close()
        if run:
            os.system(cmd)
        if docker:
            pass

    @staticmethod
    def info(info,prefix,para=1):
        md = "#"*3
        cmdfile = prefix + ".cmd"
        fp = open(cmdfile,"a")
        fp.write("\n\n")    
        line = "%s  %s --parallize %s\n\n" % (md,info,para)
        fp.write(line)
    
        fp.close()


    
