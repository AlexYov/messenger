import socket
import threading
import sqlite3
from rsa import Decrypt
from rsa import Encrypt
from rsa import Save_keys
from time import sleep
import pickle

shutdown = False
join = False

def recieve(name, sock):
    while not shutdown:
        try:
            while True:
                data, address = sock.recvfrom(4096)
                print('Собеседник: '+ Decrypt(pickle.loads(data)))
                
        except:
            pass

host = socket.gethostbyname(socket.gethostname())
port = 0

server = ('192.168.0.102',1488)

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client.bind((host,port))
client.setblocking(0)

thread1 = threading.Thread(target = recieve, args = ('recieve_data',client))
thread1.start()

while shutdown == False:   
    
    if join == False:
        Save_keys()
        join = True
        
    elif join == True:
        #try:
        message = input('Text: ')
        if message != '':
            enc_message = pickle.dumps(Encrypt(message.encode('utf-8')))
            client.sendto(enc_message,server)
            print('Вы: ' + message)
        sleep(0.2)
        #except:
            #shutdown = True
            
     
thread1.join()
client.close()
    

