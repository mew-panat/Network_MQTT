from socket import * 
import pickle
import sys

MAX_BUF = 2048
SERV_PORT = 50000

def main():
    cur_ip = 0
    while True:
        txtin = sys.stdin.readline().strip().split()  
        if txtin[0] == 'quit' and len(txtin) == 1 :
            exit()
        elif len(txtin) != 4:
            print('You must enter 4 arguments: subscribe broker_ip_address topic_name data_to_publish')
        else:
            role = txtin[0]
            ip = txtin[1]
            topic = txtin[2]
            data = txtin[3]
                
            if ip != cur_ip:
                addr = (ip, SERV_PORT)
                s = socket(AF_INET, SOCK_STREAM)
                s.connect(addr)
                cur_ip = ip

            sys.stdout.flush()
            txtout = (role,topic,data)
            data_string = pickle.dumps(txtout)
            s.send(data_string)
            check = s.recv(MAX_BUF)
            msg = pickle.loads(check)
            if msg != 'quit':
                print(msg)
            else:                
                exit() 
    s.close()

if __name__ == '__main__':
    main()    