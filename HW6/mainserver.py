import socket
import pickle
import hashlib
import random
import string
import threading

from honeychecker import HoneyChecker
from config import *

class server:
    def __init__(self, HC_PORT):
        self.database = {}                      # Password database
        self.salts = {}                         # User salt database

    # HoneyWord generation algorithm
    def generate_honeywords(self, user_id, password):
        honeywords = []

        while True:
            salt = ''.join(random.choice(string.ascii_letters + string.digits) for i in range(SALT_LENGTH))
            if salt not in self.salts.values():
                break
        
        # DEFAULT HONEYWORD
        pwd_hash = hashlib.sha256((DEFAULT_HONEYWORD + salt).encode('utf-8')).hexdigest()
        honeywords.append(pwd_hash)
        
        # REAL PASSWORD
        pwd_hash = hashlib.sha256((password + salt).encode('utf-8')).hexdigest()
        honeywords.append(pwd_hash)
        
        # LIST OF HONEYWORDS
        for i in range(NUM_PWD):
            honeyword = hashlib.sha256((password + str(i) + salt).encode('utf-8')).hexdigest()
            honeywords.append(honeyword)
            
        random.shuffle(honeywords)
        pwd_idx = honeywords.index(pwd_hash)

        # Create server socket and connect to honeychecker
        hc_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        hc_socket.connect(('localhost', HC_PORT))

        # Send update account request to honeychecker
        request = {'type': 'update', 'user_id': user_id, 'password': pwd_idx}
        hc_socket.send(pickle.dumps(request))

        # Receive honeychecker response
        response = pickle.loads(hc_socket.recv(BUFFER_SIZE))
        print(f"STATUS: {response['message']}\n")

        # Close server socket
        hc_socket.close()

        return salt, honeywords

    # HoneyChecker
    def is_honeyword(self, user_id, pwd_hash):
        pwd_idx = self.database[user_id].index(pwd_hash)

        # Create server socket and connect to honeychecker
        hc_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        hc_socket.connect(('localhost', HC_PORT))

        # Send create account request to honeychecker
        request = {'type': 'check', 'user_id': user_id, 'password': pwd_idx}
        hc_socket.send(pickle.dumps(request))

        # Receive honeychecker response
        response = pickle.loads(hc_socket.recv(BUFFER_SIZE))
        print(f"STATUS: {response['message']}\n")

        # Close server socket
        hc_socket.close()
        
        result = response['result']

        return result

    # Alert mechanism
    def send_alert(self, user_id, honeyword):
        print(f"ALERT: User {user_id}'s account has been compromised with HoneyWord \"{honeyword}\"\n")

    # Handle client requests
    def handle_client(self, client_socket):
        # Receive client request
        request = pickle.loads(client_socket.recv(BUFFER_SIZE))

        if request['type'] == 'create':
            # Create new account
            user_id = request['user_id']
            password = request['password']
            salt, honeywords = self.generate_honeywords(user_id, password)
            
            # Update local database
            self.database[user_id] = honeywords
            self.salts[user_id] = salt
            
            response = {'status': 'success', 'message': 'Account created successfully'}
            client_socket.send(pickle.dumps(response))

        elif request['type'] == 'authenticate':
            # Authenticate user
            user_id = request['user_id']
            password = request['password']
            
            if user_id not in self.database.keys():
                response = {'status': 'fail', 'message': 'User ID not found'}
                print(f"STATUS: {response['message']}\n")
                client_socket.send(pickle.dumps(response))
            else:
                pwd_hash = hashlib.sha256((password + self.salts[user_id]).encode('utf-8')).hexdigest()
                honeywords = self.database[user_id]

                if pwd_hash in honeywords:
                    if self.is_honeyword(user_id, pwd_hash):
                        self.send_alert(user_id, password)
                        response = {'status': 'fail', 'message': 'Invalid password'}
                        client_socket.send(pickle.dumps(response))
                    else:
                        response = {'status': 'success', 'message': 'Authentication successful'}
                        client_socket.send(pickle.dumps(response))

                else:
                    response = {'status': 'fail', 'message': 'Invalid password'}
                    print(f"STATUS: {response['message']}\n")
                    client_socket.send(pickle.dumps(response))

        # Close client socket
        client_socket.close()

    def run(self):
        # Create server socket
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(('localhost', SERVER_PORT))
        server_socket.listen(5)
        print(f"Server started on port {SERVER_PORT}...")

        # Accept client connections and handle requests
        while True:
            client_socket, address = server_socket.accept()
            print("Connection established with client %s" % str(address))
            self.handle_client(client_socket)

def main():
    HC = HoneyChecker()
    srv = server(HC_PORT)

    HC_thread = threading.Thread(target=HC.run)
    srv_thread = threading.Thread(target=srv.run)

    HC_thread.start()
    srv_thread.start()

    
if __name__ == '__main__':
    main()