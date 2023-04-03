import socket
import pickle

from config import *

# Create account function
def create_account(user_id, password):
    # Create client socket and connect to server
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', SERVER_PORT))

    # Send create account request to server
    request = {'type': 'create', 'user_id': user_id, 'password': password}
    client_socket.send(pickle.dumps(request))

    # Receive server response
    response = pickle.loads(client_socket.recv(BUFFER_SIZE))
    print(response['message'])

    # Close client socket
    client_socket.close()

# Authenticate function
def authenticate(user_id, password):
    # Create client socket and connect to server
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', SERVER_PORT))

    # Send create account request to server
    request = {'type': 'authenticate', 'user_id': user_id, 'password': password}
    client_socket.send(pickle.dumps(request))

    # Receive server response
    response = pickle.loads(client_socket.recv(BUFFER_SIZE))
    print(response['message'])

    # Close client socket
    client_socket.close()

def help():
    print("Client Action:")
    print("1 - Create Account")
    print("2 - Authenticate Account")
    print("3 - Quit")

def main():
    help()
    while True:
        action = input("\nSelect action to perform:")

        if action == "1":
            print("\nCreating account")
            user_id = input("Username:")
            password = input("Password:")
            create_account(user_id, password)

        elif action == "2":
            print("\nAuthenticating account")
            user_id = input("Username:")
            password = input("Password:")
            authenticate(user_id, password)

        elif action == "3":
            print("\nQuitting Client Session")
            break

        else:
            print("\nERROR: INVALID ACTION")
            print("Please enter a valid client action.\n")
            help()

if __name__ == '__main__':
    main()