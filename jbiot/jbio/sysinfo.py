import subprocess

def meminfo():
    mem = {}
    f = open("/proc/meminfo")
    lines = f.readlines()
    f.close()
    for line in lines:
        if len(line) < 2: continue
        name = line.split(':')[0]
        var = line.split(':')[1].split()[0]
        mem[name] = long(var) / (1024*1024.0)
    mem['MemUsed'] = mem['MemTotal'] - mem['MemFree'] - mem['Buffers'] - mem['Cached']
    total = str(round(mem["MemTotal"],2)) + "G"
    used = str(round(mem["MemUsed"],2)) + "G"
    free  = str(round(mem["MemFree"],2)) + "G"
    memstr = "MemUsed:%s\nMemFree:%s\nMemTotal:%s" % (used,free,total)
    return memstr


def cpuinfo():
    cpu = []
    cpuinfo = {}
    f = open("/proc/cpuinfo")
    lines = f.readlines()
    f.close()
    ncpu = 0
    for line in lines:
        if line.startswith("processor"):
            ncpu = ncpu + 1
    p = subprocess.Popen("top -bi -n 1 | grep Cpu",shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)  
    std = p.stdout.read()  
    used  = std.strip().split(",")[0].split(":")[1]
    used = used.strip("us").strip() + "%"
    p = subprocess.Popen("uptime",shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE) 
    std = p.stdout.read()
    avg = std.strip().split(":")[-1]
    
    cpustr = "CpuNum:%s\nCpuUsed:%s\nCpuLoad:%s"  % (ncpu,used,avg)

    return cpustr



def diskinfo():

    p = subprocess.Popen("df -h | awk '{print $5,$6}'",shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    std = p.stdout.read()
    
    return std

