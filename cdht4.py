import threading
import time
import sys
from socket import *
import re

exitFlag = 0
portbase = 50000
pingrate = 1
peer_id1 = int(sys.argv[1])
peer_id2 = int(sys.argv[2])
peer_id3 = int(sys.argv[3])
port = peer_id1+portbase
successor1_port = peer_id2+portbase
successor2_port = peer_id3+portbase
myaddress = ('127.0.0.1',port)
successor1_Addr = ('127.0.0.1',successor1_port)
successor2_Addr = ('127.0.0.1',successor2_port)
list_of_prepeer=[]

#class of peer
class Peer(object):
    def __init__(self):
        self.cur_id = peer_id1
        self.next1 = peer_id2
        self.next2 = peer_id3
        self.prev1 = None
        self.prev2 = None
        self.alive = 1

    def get_next1(self):
        return self.next1

    def get_next2(self):
        return self.next2

    def is_alive(self):
        if self.alive == 1:
            return 1
        else:
            return 0

p = Peer()

#UDPserver
def UDPServer():
    ADDR = ('127.0.0.1',port)
    sock = socket(AF_INET ,SOCK_DGRAM)
    sock.bind(ADDR)
    while 1:
        #time.sleep(1)
        data_of_client,client_addr= sock.recvfrom(1024)
        msg = data_of_client.decode()
        sq = msg[1:4]
        print (msg[4:])
        if int(data_of_client[50:]) not in list_of_prepeer:
               list_of_prepeer.append(int(data_of_client[50:]))
        if len(list_of_prepeer) == 2:
            list_of_prepeer.sort()
            pre_peer1 = list_of_prepeer[0]
            pre_peer2 = list_of_prepeer[1]
            p.prev1 = pre_peer1
            p.prev2 = pre_peer2
        if msg[0:1] == '1':
            p.prev2 =int(data_of_client[50:])
        if msg[0:1] == '2':
            p.prev1 =int(data_of_client[50:])
        #print('Peer:',p.prev1,p.prev2,p.cur_id,p.next1,p.next2)
        udpservermessage = msg[0:1]+str(p.next1+50000)+str(p.next2+50000)+'A ping response message was received from Peer {0}'.format(peer_id1)
        sock.sendto(udpservermessage.encode(), client_addr)
    sock.close()



#UDPclient1
def UDPClient1(p1,p2):
    sq1 = 100
    s1_p = int(p1)+50000
    ADDR1 = (('',s1_p))
    n1 = 0
    sock1 = socket(AF_INET ,SOCK_DGRAM)
    while 1:
        livestate = p.is_alive()
        if livestate != 1:
            break
        time.sleep(2)
        sock1.settimeout(1)
        try:
            udpclientmessage = '1' + str(sq1)+'A ping request message was received from Peer {0}'.format(peer_id1)
            if sq1 <=999:
                sq1 += 1
            else:
                sq1 = 100
            p1 = p.get_next1()
            ADDR1 = (('',int(p1)+50000))
            sock1.sendto(udpclientmessage.encode(), ADDR1)
            data_of_server1, server_addr1 = sock1.recvfrom(1024)
            msg_of_server1 =data_of_server1.decode()
            print(msg_of_server1[11:])
            p1 = p.get_next1()
            ADDR1 = (('',int(p1)+50000))
        except Exception:
            n1+=1
            if n1==4:
                if msg_of_server1[0:1] == '1':
                    p.next1 = int(msg_of_server1[1:6])-50000
                    p.next2 = int(msg_of_server1[6:11])-50000
                    ADDR1 = int(p.next1)+50000
                    ADDR2 = int(p.next2)+50000
                if msg_of_server1[0:1] == '2':
                    p.next2 =int(msg_of_server1[1:6])-50000
                    ADDR2 = int(p.next2)+50000
                print('Peer {0} is no longer alive'.format(msg_of_server1[57:]))
                print('My first successor is now peer {0}'.format(p.next1))
                print('My second successor is now peer {0}'.format(p.next2))
    sock1.close()


def UDPClient2(p1,p2):
    sq2 = 100
    s2_p = int(p2)+50000
    ADDR2 = (('',s2_p))
    n2 = 0
    sock2 = socket(AF_INET ,SOCK_DGRAM)
    while 1:
        livestate = p.is_alive()
        if livestate != 1:
            break
        time.sleep(2)
        sock2.settimeout(1)
        try:
            udpclientmessage = '2'+str(sq2)+'A ping request message was received from Peer {0}'.format(peer_id1)
            if sq2 <=999:
                sq2 += 1
            else:
                sq2 = 100
            p2 = p.get_next2()
            ADDR2 = (('',int(p2)+50000))
            sock2.sendto(udpclientmessage.encode(), ADDR2)
            data_of_server2, server_addr2 = sock2.recvfrom(1024)
            msg_of_server2 =data_of_server2.decode()
            print(msg_of_server2[11:])
            p2 = p.get_next2()
            ADDR2 = (('',int(p2)+50000))
        except Exception:
            n2+=1
            if n2==4:
                if msg_of_server2[0:1] == '1':
                    p.next1 = int(msg_of_server2[1:6])-50000
                    p.next2 = int(msg_of_server2[6:11])-50000
                    ADDR1 = int(p.next1)+50000
                    ADDR2 = int(p.next2)+50000
                if msg_of_server2[0:1] == '2':
                    p.next2 =int(msg_of_server2[1:6])-50000
                    ADDR2 = int(p.next2)+50000
                print('Peer {0} is no longer alive'.format(msg_of_server2[57:]))
                print('My first successor is now peer {0}'.format(p.next1))
                print('My second successor is now peer {0}'.format(p.next2))
    sock2.close()


#TCPserver
def TCPserver():
    sock = socket(AF_INET ,SOCK_STREAM)
    sock.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
    sock.bind(('',port))
    sock.listen(10)
    while 1:
        conn,addr = sock.accept()
        data_ori = conn.recv(1024)
        data = data_ori.decode()
        if data[0:2] == 'NB':
            file_name = int(data[7:])
            flag = 0
            file_id =int(file_name)%256
            if peer_id2<peer_id1 and file_id>=peer_id1:   #calculate the peer which store file
                flag = 1
            elif file_id<peer_id2:
                if file_id >= peer_id1:
                    flag = 1
                if peer_id2<peer_id1:
                    flag = 1
            if flag == 1: #file is in current peer
                print('File {0} is here.\nA response message,destined for peer {1},has been sent'.format(file_name,peer_id1))
                filemsg_to_source = 'Sourceport'+data[2:]
                sent_to_source = threading.Thread(target=send_file_request_to_source, args=[filemsg_to_source])
                sent_to_source.start()#source_addr need to be identified
            else:        #send find file msg to successor peer
                print('File {0} is not here.\nFile request message has been forwarded to my successor'.format(file_name))
                sent_to_successor = threading.Thread(target=send_file_request_to_successor, args=[data])
                sent_to_successor.start()  
        if data[:10] == 'Sourceport':
            for i in range(len(data)):
                if data[i] == 'i':
                    dest_id = data[i+2:]
                    file_name2 = data[15:i]
            print('Received a response message from peer {0}, which has the file {1}'.format(dest_id,file_name2))
        if data[0:4] == 'quit':  #receive graceful quit msg
            for i in range(len(data)):
                if data[i] == 'n':
                    n = i
                    leave_peer = data[4:n]
                    next_peer_of_leave_peer = data[n+1:]
            if int(leave_peer) == p.next1:
                p.next1 = p.next2
                p.next2 = int(next_peer_of_leave_peer)
            if int(leave_peer) == p.next2:
                p.next2 = int(next_peer_of_leave_peer)
            print('Peer {0} will depart from the network'.format(data[4:n]))
            print('My first successor is now peer {0}'.format(p.next1))
            print('My second successor is now peer {0}'.format(p.next2))
        time.sleep(1)
#conn.send(b"server has received your msg")
    sock.close()


#input lines to decide file_transmit or graceful quit
def read_in():
    try:
        while True:
            lines = sys.stdin.readline().strip('\n')
            #print('lines2',lines)
            if lines[0:4] == 'File':
                m = re.compile('\d{1,9}')
                file_name = re.findall(m,lines)
                #print('file_name2:',file_name[0])
                sent_f = threading.Thread(target=filetransmit, args=[file_name[0]])
                sent_f.start()
            elif lines == 'quit':
                sent_t1= threading.Thread(target=send_graceful_msg_to_prepeer1, args=[lines])
                sent_t2= threading.Thread(target=send_graceful_msg_to_prepeer2, args=[lines])
                sent_t1.start()
                sent_t2.start()
                p.alive = 0
    except:
        pass

#send first file transmit message
def filetransmit(file_name):
    flag = 0
    file_name = file_name
    file_id =int(file_name)%256
    print('file_id:',file_id)
    if peer_id2<peer_id1 and file_id>=peer_id1:   #calculate the peer which store file
        flag = 1
    elif file_id<peer_id2:
        if file_id >= peer_id1:
            flag = 1
        if peer_id2<peer_id1:
            flag = 1
    if flag == 1: #file is in current peer
        #print('flag == 1\n')
        print('File {0} is here.\nA response message,destined for peer {1},has been sent'.format(file_name,peer_id1))
        filemsg_to_source = 'Received a response message from peer {0}, which has the file {1}'.format(peer_id1,file_name)
        sent_to_source = threading.Thread(target=send_file_request_to_source, args=[filemsg_to_source])
        sent_to_source.start()#source_addr need to be identified
    else:        #send find file msg to successor peer
        #print('flag == 0\n')
        print('File {0} is not here.\nFile request message has been forwarded to my successor'.format(file_name))
        source_port = port
        msg_to_successor = 'NB' + str(port) + str(file_name)
        sent_to_successor = threading.Thread(target=send_file_request_to_successor, args=[msg_to_successor])
        sent_to_successor.start()   
    
#TCPclient
def send_file_request_to_successor(lines):
    sock = socket(AF_INET ,SOCK_STREAM) 
    time.sleep(1)
    successor1_port = p.next1 + 50000
    sock.connect(('',successor1_port))
    while 1:
        time.sleep(1)
        sock.send(lines.encode())
        data_from_server = sock.recv(1024)
        print(data_from_server)
    sock.close()
    
def send_file_request_to_source(lines):
    if lines[0:10] == 'Sourceport':
        source_port = int(lines[10:15])
    lines = lines +'id'+str(peer_id1)
    sock = socket(AF_INET ,SOCK_STREAM) 
    time.sleep(1)
    sock.connect(('',source_port))
    while 1:
        time.sleep(1)
        sock.send(lines.encode())
        data_from_server = sock.recv(1024)
        print(data_from_server)
    sock.close()

def send_graceful_msg_to_prepeer1(lines):
    sock = socket(AF_INET ,SOCK_STREAM)
    time.sleep(1)
    pre_peer1_port = p.prev1+portbase
    sock.connect(('',pre_peer1_port))
    lines = lines + str(p.cur_id) + 'n' + str(p.next1)
    while 1:
        time.sleep(1)
        sock.send(lines.encode())
        data_from_server = sock.recv(1024)
        print(data_from_server)
    sock.close()

def send_graceful_msg_to_prepeer2(lines):
    sock = socket(AF_INET ,SOCK_STREAM)
    time.sleep(1)
    pre_peer2_port = p.prev2+portbase
    sock.connect(('',pre_peer2_port))
    lines = lines + str(p.cur_id) + 'n' + str(p.next2)
    while 1:
        time.sleep(1)
        sock.send(lines.encode())
        data_from_server = sock.recv(1024)
        print(data_from_server)
    sock.close()
    

myinput = threading.Thread(target=read_in)
UDPcli1 = threading.Thread(target=UDPClient1,args=[p.get_next1(),p.get_next2()])
UDPcli2 = threading.Thread(target=UDPClient2,args=[p.get_next1(),p.get_next2()])
UDPser = threading.Thread(target=UDPServer)
TCPser = threading.Thread(target=TCPserver)
myinput.start()
TCPser.start()
UDPcli1.start()
UDPcli2.start()
UDPser.start()





