from socket import *
from socket import SHUT_RDWR
import sys
import pickle
import os
from threading import Thread

MAX_BUF = 2048
SERV_PORT = 50000

data = None
def handle_exit(s):  
    txtin = sys.stdin.readline().strip().split() 
    if txtin[0] == 'quit':
        s.send(pickle.dumps(txtin))               
    else:
        print('You can subscribe only 1 topic')
    

def main():
    txtin = sys.stdin.readline().strip().split()  
    while (len(txtin) != 3) :
        print('You must enter 3 arguments: subscribe broker_ip_address topic_name')
        txtin = sys.stdin.readline().strip().split()  
    else:
        role = txtin[0]
        ip = txtin[1]
        topic = txtin[2]

        addr = (ip, SERV_PORT)
        s = socket(AF_INET, SOCK_STREAM)
        s.connect(addr)      

        txt_data = (role, topic, data)
        data_string = pickle.dumps(txt_data)
        sys.stdout.flush()
        s.send(data_string)

        while True: 
            th = Thread(target=handle_exit,args=(s,))
            th.daemon = True
            th.start()

            modifiedMsg = s.recv(MAX_BUF)
            msg = pickle.loads(modifiedMsg)    
            if msg != 'quit':
                print(msg)
            else:                                  
                s.close() 
                sys.exit(0)
        s.close() 

if __name__ == '__main__':
    main()      

