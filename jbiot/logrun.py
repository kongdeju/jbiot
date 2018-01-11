import os

class log:

    @staticmethod
    def run(cmd,prefix="run",run=False,docker=False):

        cmdfile = prefix + ".cmd"
        fp = open(cmdfile,"a")
        #cmd = '''    echo  "%s" ;%s''' % (cmd,cmd)
        cmd = "    %s" % cmd
        line = cmd + "\n"
        fp.write(line)

        fp.close()
        if run:
            os.system(cmd)
        if docker:
            pass

    @staticmethod
    def info(info,prefix,para=1,mem="2G"):
        md = "#"*3
        cmdfile = prefix + ".cmd"
        fp = open(cmdfile,"a")
        fp.write("\n\n")    
        line = "%s  %s --para=%s --mem=%s\n\n" % (md,info,para,mem)
        fp.write(line)
    
        fp.close()


    
