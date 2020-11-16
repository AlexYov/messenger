import socket
from time import sleep
import psycopg2
import threading

class Server:
        def __init__(self,host,port):     
                self.host = host
                self.port = port
                self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.server.bind((self.host,self.port))
                self.server.listen(0)
                print('Server started')
                self.conn = sqlite3.connect("database.db", check_same_thread = False)
                self.cursor = self.conn.cursor()
                self.cursor.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, sock inet);')
                threading.Thread(target = self.accept_data).start()
                
        def accept_data(self):
                while True:
                        client, address = self.server.accept() 
                        #print(client)
                        print(address)         
                        self.cursor.execute('SELECT sock FROM users;')
                        users = self.cursor.fetchall()
                        if client not in users:
                                self.cursor.execute('INSERT INTO users(sock) VALUES (?);',(client,))
                                self.conn.commit()  
                        
                        threading.Thread(target = self.send_data, args = (client,)).start()
                sleep(0.1)
                                     
        def send_data(self,client):
                while True:
                        data = client.recv(4096) 
                        #print(data)
                        self.cursor.execute('SELECT sock FROM users;')
                        list_socks = self.cursor.fetchall()
                        #print(list_clients)
                        #print(client)
                        for sock in list_socks:
                                #print(client0)
                                if client == sock:
                                        sock.send(data)
                sleep(0.1)

host = socket.gethostbyname(socket.gethostname())
print(host)
port = 1488 
Server(host,port)

        
