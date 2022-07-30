import os,time
from socket import *
server=socket(AF_INET,SOCK_DGRAM)
if os.path.isfile('.tempipconnection'):
    ip=str(input('['+str(open('.tempipconnection').read().replace('\n',''))+'] IP:'))
    if len(ip)==0:
        ip=open('.tempipconnection').read().replace('\n','')
        print('Connecting',str(ip),'...')
else:
    ip=str(input('IP:'))
x=open('.tempipconnection','w')
x.write(ip)
x.close()
#ip='127.0.0.1'
byte=0
def crypt(msg):
    msg=msg[::-1]
    tmp=b''
    for a in msg:
        tmp+=int(255-a).to_bytes(1,'big')
    return tmp
def halt():
    global wait,byte
    byte=0
    while wait:
        tmp=crypt(server.recvfrom(4096)[0])
        byte+=len(tmp)
        tmp=tmp.decode('utf-8')
        if tmp=='EOL':
            wait=0
        if wait:
            print(tmp)
server.sendto(crypt(bytes('motd','utf-8')),(ip,7000))
wait=0
tmp=crypt(server.recvfrom(4096)[0])
server.settimeout(30)
psd='No Name'
if tmp.decode('utf-8')=='SOL':
    wait=1
    halt()
while True:
    try:
        server.sendto(crypt(bytes('psd','utf-8')),(ip,7000))
        wait=0
        tmp=crypt(server.recvfrom(4096)[0])
        if tmp.decode('utf-8')=='SOL':
            wait=1
        while wait:
            tmp=crypt(server.recvfrom(4096)[0])
            tmp=tmp.decode('utf-8')
            if tmp=='EOL':
                wait=0
            if wait:
                psd=tmp
        tmp=''
        cmd=str(input(str(psd)))
        server.sendto(crypt(bytes(cmd,'utf-8')),(ip,7000))
        wait=0
        tmp=crypt(server.recvfrom(4096)[0])
#        print('['+str(tmp)+']')
        if tmp.decode('utf-8')=='SOL':
            wait=1
            halt()
    except Exception:
        continue    
