from socket import *
from threading import Thread
import pickle
import os
import sys

MAX_BUF = 2048
SERV_PORT = 50000
MAX_CONNECT = 10

#create Python Dictionaries to keep all subscriber 
subscriber_list = {}
def handle_client(s,addr):
    while True:
        try:
            txtin = s.recv(MAX_BUF)
            data = pickle.loads(txtin)
            ip, port = str(addr[0]), str(addr[1])    
            if data[0] == 'quit':
                handle_exit(s,ip,port)
                break
            else:
                role, topic, msg = data
                if role == 'subscribe':             
                    print('New subscriber connected from ..' + ip + ':' + port) 
                    if topic in subscriber_list:
                        subscriber_list[topic].append(s)
                    else:        
                        subscriber_list[topic] = [s]    

                elif role == 'publish': 
                    print('New publisher connected from ..' + ip + ':' + port) 
                    if topic not in subscriber_list:
                        wait_loop(s,topic)     
                        
                    elif topic in subscriber_list:
                        wait_publisher(s, topic, msg)         
        except EOFError:            
            handle_exit(s,ip,port)  
            break
    s.close()
    return

def handle_exit(s,ip,port):    
    i = 0
    msg = ('quit')
    print('Terminate connection ..' + ip + ':' + port) 
    for x in subscriber_list:
        if x in subscriber_list:
            topic = x
    for sub_s in subscriber_list[topic]:
        if s in subscriber_list[topic]:
            del subscriber_list[topic][i]
        i += 1
    if not bool(subscriber_list[topic]):
        del subscriber_list[topic]
    s.send(pickle.dumps(msg))
 
def wait_loop(s,topic):
    msg = pickle.dumps(('No subscribers subscribe ' + topic + ' ...'))
    s.send(msg)
    
def wait_publisher(s, topic,msg):    
    s.send(pickle.dumps('Publish! ' + topic + ':' + msg))    
    handle_publisher(topic, msg)  

def handle_publisher(topic,msg):    
    msg = ('Subscribe! '+ topic + ':' + msg)    
    data = pickle.dumps(msg)      
    if topic in subscriber_list:
        for sub_s in subscriber_list[topic]:  
            sub_s.send(data)           
                
def main():
    addr = ('127.0.0.1', SERV_PORT)
    s = socket(AF_INET, SOCK_STREAM)
    s.bind(addr)
    s.listen(MAX_CONNECT)
    print('TCP threaded server started ...')

    while True:
        sckt, addr = s.accept()
        try:
            Thread(target=handle_client, args=(sckt,addr)).start()
        except:
            print("Cannot start thread..")
            import traceback
            traceback.print_exc()

    s.close()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('quit ..')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)