import os,urllib.request,sys,psutil,subprocess,platform
from socket import *
#forbid=['sudo','user','apt','htop','exit','bash','py',':','&','su','man']
forbid=['analsyde']
rootfs='rootfs/'
binpath=rootfs+'bin/'
libpath=rootfs+'lib/'
x16path=rootfs+'16x/'
sharepath=rootfs+'share/'
settingspath=rootfs+'etc/'
homepath=rootfs+'user/'
path=[rootfs,binpath,libpath,sharepath,x16path,settingspath,homepath]
version=0.2*1
rpnt=print
osname='LShell'
motd='Welcome to '+str(os.name).upper()+' '+str(platform.release())
def execute(cmd):
    popen = subprocess.Popen(cmd, stdout=subprocess.PIPE, universal_newlines=True)
    for stdout_line in iter(popen.stdout.readline, ""):
        yield stdout_line
    popen.stdout.close()
    return_code = popen.wait()
    if return_code:
        raise subprocess.CalledProcessError(return_code, cmd)
def encrypt(msg):
    tmp=b''
    for a in msg:
        print(a)
        tmp+=int(255-a).to_bytes(1,'big')
    return tmp
def pnt(msg):
    rpnt(str(msg)+' to ('+str(address)+')')
    server.sendto(bytes(msg,'utf-8'),address)
def abr(size):
    if size>=1000000000000:
        return str(size//1000000000000)+' TB'
    elif size>=1000000000:
        return str(size//1000000000)+' GB'
    elif size>=1000000:
        return str(size//1000000)+' MB'
    elif size>=1000:
        return str(size//1000000)+' KB'
    else:
        return str(size)+' B'
def xshell(cmd):
    pnt('SOL')
    pnt(subprocess.check_output(cmd, shell=True).decode().strip())
    pnt('EOL')
def shell(cmd):
    arg=[]
    cmd=cmd.replace('\n','')
    legacycmd=cmd
    cmd=cmd.split(' ')
    #if len(cmd)>1:
    #    arg=cmd[1:]
    #cmd=cmd[0]
    pnt('SOL')
    if cmd[0]=='ramstat':
        pnt('Total Ram:'+str(abr(psutil.virtual_memory()[0])))
        pnt('Free Ram:'+str(abr(psutil.virtual_memory()[1])))
        pnt('Used Ram:'+str(abr(psutil.virtual_memory()[3])))
    elif cmd[0]=='motd':
        pnt(motd)
    elif cmd[0]=='path':
        pnt('Paths:')
        for a in path:
            a=a.replace('\n','')
            pnt(a)
    elif cmd[0]=='osstat':
        pnt(str(os.name).upper()+' '+str(platform.release()))
    elif cmd[0]=='containerstat':
        pnt(osname+' '+str(version)+'\nBuilt on 07/25/2022')
    elif cmd[0]=='cpustat':
        pnt('CPU USAGE:'+str(psutil.cpu_percent())+'%')
    else:
        accept=False
        for a in os.listdir(binpath):
            if cmd in a:
                pnt(a)
                if os.path.isfile(binpath+a):
                    accept=True
                    try:
                        exec(open(binpath+a).read())
                        break
                    except Exception:
                        pnt('Segmentation Error')
        if not accept:
#            pnt('Unknown Command '+str(cmd))
            accept=False
            for b in forbid:
                if b in legacycmd:
                    accept=False
                    break
                else:
                    accept=True
            if accept:
#                pnt(subprocess.check_output(legacycmd, shell=True).decode().strip())
#                tmp=subprocess.getoutput(legacycmd).split('\n')
                for a in execute(cmd):
                    a=a.replace('\n','')
                    pnt(a)
            else:
                pnt('This is Disabled Cause: in Forbid Section')
    pnt('EOL')
def create_user(user):
    if not os.path.isdir(homepath+user):
        os.mkdir('')
    else:
        pnt(user+' Already Exists')
for a in path:
    if not os.path.isdir(a):
        os.mkdir(a)
        rpnt('Created '+a)
rpnt('Starting',osname,'Remote Server... (25072022)')
server=socket(AF_INET,SOCK_DGRAM)
server.bind(('0.0.0.0',7000))
rpnt('Started on 0.0.0.0 7000')
while True:
    message, address=server.recvfrom(4096)
    try:
        message.decode('utf-8')
        shell(message.decode('utf-8'))
    except Exception as error:
        pnt(str(error))
#    rpnt(address)
