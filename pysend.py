
import socket
import sys
import os
from os.path import expanduser, join


MAX=65536
PORT=1060
BASE_PATH='~/Downloads/pysend/'
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

def findfreename(name,folder):
    i=1
    while os.path.exists(join(expanduser(BASE_PATH),'.'.join(name.split('.')[:-1])+'(%d)'%i+'.'+name.split('.')[-1])):
        i+=1
    return '.'.join(name.split('.')[:-1])+'(%d)'%i+'.'+name.split('.')[-1]
        

def recvall(sock, length):
    data = b''
    name=''
    flag = 0
    while True:
        more=sock.recv(1)
        if more=='\r':
            flag+=1
            length=len(data)+int(data)
            l2=length
            print 'the file is %d bytes long' %length
            break
        data+=more
    while True:
        more=sock.recv(1)
        if more=='\r':
            print 'the name is %s' %name
            length=len(data)+int(data)
            recvmessage(sock,l2,name)
            break
        name+=more
    return l2
    
    
def recvmessage(sock,length,name):
    f=None
    if os.path.exists(join(expanduser(BASE_PATH),name)):
        c=raw_input('overwrite? (Y/n) : ')
        if c=='Y' or c=='y':
            f=open(join(expanduser(BASE_PATH),name),'a')
        else :
            f=open(join(expanduser(BASE_PATH),findfreename(name,expanduser(BASE_PATH))),'a')
    else:
        f=open(join(expanduser(BASE_PATH),name),'a')
    data = b''
    donel=0
    flag = 0
    while donel < length:
        more = sock.recv(MAX)
        if not more:
            break
        f.write(more)
        donel+=len(more)
        sys.stdout.flush()
        sys.stdout.write("\r%d%% done" % (donel*100/(length-10)))
        
        
if len(sys.argv)==2 and sys.argv[1]=='receive':
    print 'press ctrl+c to stop receiving files'
    if not os.path.isdir(expanduser(BASE_PATH)):
        os.makedirs(expanduser(BASE_PATH))
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('',1060))
    s.listen(1)
    while True:
        sc,sockname=s.accept()
        print '\nnew connection received'
        data=recvall(sc,MAX)
        sys.stdout.flush()
        print("\nfile received")
        sc.close()
elif len(sys.argv)==4 and sys.argv[1] == 'send':
    s.connect((sys.argv[2], PORT))
    print 'sending to ' + sys.argv[2] + ':' + str(PORT)
    path=sys.argv[3]
    f=open(path,'rb')
    size=os.path.getsize(path)
    s.send(str(size)+'\r'+path.split('/')[-1]+'\r')
    i=0
    while True:
        m=f.read(MAX)
        if m=='':
            break
        s.sendall(m)
        i += 1
        if not size<MAX:
            sys.stdout.flush()
            sys.stdout.write('\r%d%% sent' %(MAX*i*100/size))
        else:
            print 'done'
            s.close()
            exit(0)
    print ' '  
    s.close()
else :
    print 'usage > send|receive [address] [file]'
        

