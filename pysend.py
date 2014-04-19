
import socket,sys,os
from os.path import expanduser, join
PORT=1060
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
def findfreename(name,folder):
    i=1
    while os.path.exists(join(expanduser('~/Downloads/pysend'),'.'.join(name.split('.')[:-1])+'(%d)'%i+'.'+name.split('.')[-1])):
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
            
            recvall2(sock,l2,name)
            break
        name+=more
        
    
    return l2
def recvall2(sock,length,name):
    f=None
    if os.path.exists(join(expanduser('~/Downloads/pysend/'),name)):
        c=raw_input('overwrite? (Y/n) : ')
        if c=='Y' or c=='y':
            f=open(join(expanduser('~/Downloads/pysend/'),name),'a')
        else :
            f=open(join(expanduser('~/Downloads/pysend/'),findfreename(name,expanduser('~/Downloads/pysend/'))),'a')
    else:
        f=open(join(expanduser('~/Downloads/pysend/'),name),'a')
    
    data = b''
    donel=0
    flag = 0
    while donel < length:
        more = sock.recv(65536)
        if not more:
            break
        f.write(more)
        donel+=len(more)
        sys.stdout.flush()
        sys.stdout.write("\r%d%% done" % (donel*100/(length-10)))
if len(sys.argv)==2 and sys.argv[1]=='receive':
    print 'press ctrl+c to stop receiving files'
    if not os.path.isdir(expanduser('~/Downloads/pysend')):
        os.makedirs(expanduser('~/Downloads/pysend'))
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('',1060))
    s.listen(1)
    while True:
        
        sc,sockname=s.accept()
        
        
        
        data=recvall(sc,2**15)
        sys.stdout.flush()
        print("\nfile received")
        
        sc.close()
elif len(sys.argv)==4 and sys.argv[1] == 'send':
    s.connect((sys.argv[2], PORT))
    print('Client has been assigned socket name', s.getsockname())
    f=open(sys.argv[3],'rb')
    size=os.path.getsize(sys.argv[3])
    
    s.send(str(os.path.getsize(sys.argv[3]))+'\r'+sys.argv[3].split('/')[-1]+'\r')
    i=0
    while True:
        m=f.read(65536)
        if m=='':
            break
        s.sendall(m)
        i+=1
        if not size<65536:
            sys.stdout.flush()
        
            sys.stdout.write('\r%d%% sent' %(65536*i*100/size))
        else:
            print 'done'
            s.close()
            exit(0)
        
    
    print ' '  
    s.close()
else :
    print 'usage > send|receive [address] [file]'
        

