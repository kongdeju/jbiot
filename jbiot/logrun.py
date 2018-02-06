import os

class log:

    @staticmethod
    def run(cmd,prefix="run",run=False):
        cmdfile = prefix + ".cmd"
        fp = open(cmdfile,"a")
        #cmd = '''    echo  "%s" ;%s''' % (cmd,cmd)
        cmd = "    %s" % cmd
        line = cmd + "\n"
        fp.write(line)

        fp.close()
    
    @staticmethod
    def info(info,prefix,para=1,mem="2G",dimg=None):
        md = "#"*3
        cmdfile = prefix + ".cmd"
        fp = open(cmdfile,"a")
        fp.write("\n\n")
        if not dimg:
            line = "%s  %s --para=%s --mem=%s\n\n" % (md,info,para,mem)
        else:
            line = "%s  %s --para=%s --mem=%s --docker=%s\n\n" % (md,info,para,mem,dimg)
        fp.write(line)
        fp.close()

