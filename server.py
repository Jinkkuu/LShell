from genericpath import isdir
import os,urllib.request,sys,psutil,subprocess,platform
from socket import *
#forbid=['ping']
forbid=['analsyde']
#rootfs='rootfs/'
#binpath=rootfs+'bin/'
#libpath=rootfs+'lib/'
#x16path=rootfs+'16x/'
#sharepath=rootfs+'share/'
#settingspath=rootfs+'etc/'
#homepath=rootfs+'user/'
#path=[rootfs,binpath,libpath,sharepath,x16path,settingspath,homepath]
version=0.002*7
rpnt=print
osname='LShell'
motd='Welcome to '+str(os.name).upper()+' '+str(platform.release())
commands=['help - Show Help Page :>','osstat - Check OS Version','shellstat - Check Shell Version','cpustat - Check CPU Usage','ramstat - Check Ram Pressure']
def execute(cmd,port):
    popen = subprocess.Popen(cmd, stdout=subprocess.PIPE, universal_newlines=True)
    for stdout_line in iter(popen.stdout.readline, ""):
        yield stdout_line
    popen.stdout.close()
    return_code = popen.wait()
    if return_code:
        pass
def crypt(msg):
    msg=msg[::-1]
    tmp=b''
    for a in msg:
        tmp+=int(255-a).to_bytes(1,'big')
    return tmp
def pnt(msg):
    rpnt(str(msg)+' to ('+str(address)+')')
    server.sendto(crypt(bytes(msg,'utf-8')),address)
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
#    elif cmd[0]=='path':
#        pnt('Paths:')
#        for a in path:
#            a=a.replace('\n','')
#            pnt(a)
    elif cmd[0]=='help':
        pnt('Commands:')
        for a in commands:
            pnt(a)
    elif cmd[0]=='.'*255:
        if len(cmd)>1:
            if cmd[1]=='..':
                if os.name=='nt':
                    cwdtmp=cwd.split('\\')
                else:
                    cwdtmp=cwd.split('/')
                if not len(cwdtmp)<2:
                    cwdtmp=cwdtmp[:len(cwdtmp)-1]
                    cwd=''
                    for a in cwdtmp:                       
                        if os.name=='nt':
                            cwd+=a+'\\'
                        else:
                            cwd+=a+'/'
                    pnt('Moved to '+cwd)
                else:
                    pnt('Already at Root')
            elif os.path.isdir(cmd[1]):
                pnt('Moved to '+cmd[1])
                cwd=cmd[1]
        else:
            pnt(cwd)
    elif cmd[0]=='ls' or cmd[0]=='dir':
        for a in os.listdir():
            pnt('['+str(a)+']')
    elif cmd[0]=='connect':
        if address in adrs:
            pnt('No Need to Reconnect')
        else:
            pnt(motd)
            pnt('SET-'+psd)
    elif cmd[0]=='set':
        if not len(cmd)>1:
            pnt('Needs 2 Arguments')
        else:
            tok=''
            for a in cmd[1:]:
                tok+=a+' '
            pnt('SET-'+tok)
            
    elif cmd[0]=='osstat':
        pnt(str(os.name).upper()+' '+str(platform.release()))
    elif cmd[0]=='shellstat':
        pnt(osname+' '+str(version)+'\nBuilt on 07/29/2022')
    elif cmd[0]=='psd':
        pnt(psd)
    elif cmd[0]=='cpustat':
        pnt('CPU USAGE:'+str(psutil.cpu_percent())+'%')
    else:
#        accept=False
#        for a in os.listdir(binpath):
#            if cmd in a:
#                pnt(a)
#                if os.path.isfile(binpath+a):
#                    accept=True
#                    try:
#                        exec(open(binpath+a).read())
#                        break
#                    except Exception:
#                        pnt('Segmentation Error')
#        if not accept:
#            pnt('Unknown Command '+str(cmd))
        accept=False
        for b in forbid:
            if b in legacycmd:
                accept=False
                break
            else:
                accept=True
        if accept:
#            pnt(subprocess.check_output(legacycmd, shell=True).decode().strip())
#                tmp=subprocess.getoutput(legacycmd).split('\n')
            for a in execute(cmd,address):
                a=a.replace('\n','')
                pnt(a)
        else:
            pnt('This is Disabled Cause: in Forbid Section')
    pnt('EOL')
def engl(cmd):
    if cmd=='whoami':
        return str(address[0])
#def create_user(user):
#    if not os.path.isdir(homepath+user):
#        os.mkdir('')
#    else:
#        pnt(user+' Already Exists')
#for a in path:
#    if not os.path.isdir(a):
#        os.mkdir(a)
#        rpnt('Created '+a)
username=''
hostname=''
cwd='~'
def check():
    global username, hostname, cwd, psd
    username=str(engl('whoami'))
    hostname=str(execute('hostname','0'))
    cwd='~'
if os.path.isfile('psd'):
    rpnt('Found psd file using that as PSD')
    psd=open('psd').read().replace('\n','').replace('+cwd+',cwd).replace('+username+',username).replace('+hostname',hostname)
else:
    psd='~ $'
rpnt('Starting',osname,'Remote Server...')
server=socket(AF_INET,SOCK_DGRAM)
server.bind(('0.0.0.0',7000))
rpnt('Started on Port 7000')
adrs=[]
while 1:
    message, address=server.recvfrom(4096)
    message=crypt(message)
    try:
        message.decode('utf-8')
        if not address[0] in adrs:
            adrs=[address[0]]
            check()
        psd=open('psd').read().replace('\n','').replace('+cwd+',cwd).replace('+username+',username).replace('+hostname',hostname)
        shell(message.decode('utf-8'))
    except Exception as error:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(str(exc_tb.tb_lineno)+' Error [This is hidden to client]')
        pnt(str(error))
        pnt('EOL')
#    rpnt(address)
