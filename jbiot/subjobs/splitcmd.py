
def splitcmd(cmdfile):

    fp = open(cmdfile)
    lines = fp.readlines()
    step2cmd = {}
    step = "lsub"
    step2cmd[step] = []

    for line in lines:
        line = line.strip()
        if not line:
            continue

        if line.startswith("#"):
            step = line.strip("#").split()[0]
            step2cmd[step]  = []
        else:
            step2cmd[step].append(line)

    stepsfile = []
    i = 0
    for step,cmds in step2cmd.items():
        if not cmds:
            continue
        i = i + 1
        scmd = "step_%02d-%s.cmd" % (i,step)

        fp = open(scmd,"w")
        for cmd in cmds:
            cline = "%s\n" % cmd
            fp.write(cline)
        fp.close()
        stepsfile.append(scmd)

    return stepsfile



    
def main(args):
    pass

if __name__ == "__main__":
    import sys
    main(sys.argv[1:])





