import socket
import pickle

from config import *

class HoneyChecker():
    def __init__(self):
        self.__database = {}

    # Validate password index with honeychecker database
    def check_honeyword(self, user_id, pwd_idx):
        if self.__database[user_id] == pwd_idx:
            response = {'status': 'success', 'message': 'Password is valid.', 'result': False}
        else:
            response = {'status': 'fail', 'message': 'Password is invalid.', 'result': True}        
        return response
    
    # Update password index in honeychecker database
    def update_database(self, user_id, pwd_idx):
        self.__database[user_id] = pwd_idx
        response = {'status': 'success', 'message': 'Password updated'}
        return response
    
    def handle_server(self, server_socket):
        # Receive server request
        request = pickle.loads(server_socket.recv(BUFFER_SIZE))

        if request['type'] == 'check':
            # Check if password is valid
            user_id = request['user_id']
            password = request['password']            
            response = self.check_honeyword(user_id, password)

        elif request['type'] == 'update':
            # Add new user details to database
            user_id = request['user_id']
            password = request['password']
            response = self.update_database(user_id, password)
            
        else:
            response = {'status': 'fail', 'message': 'Invalid server request'}

        server_socket.send(pickle.dumps(response))
        
        # Close server socket
        server_socket.close()

    # Start Honeychecker
    def run(self):
        # Create server socket
        hc_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        hc_socket.bind(('localhost', HC_PORT))
        hc_socket.listen(5)
        print(f"Honeychecker started on port {HC_PORT}...")

        # Accept server connections and handle requests
        while True:
            server_socket, address = hc_socket.accept()
            print("Connection established with server %s" % str(address))
            self.handle_server(server_socket)
