import threading
import socket
import pickle
from game import *
from variables import *

host = "127.0.0.1"
port = 59007

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind((host, port))

server.listen()

def send():
    while True:
        broadcast(current_board_state)

def receive():
    while True:
        client, address = server.accept()

        if len(clients) < MAX_PLAYERS:
            print(f'connection is established with {str(address)}')
            client.send('alias?: '.encode('utf-8'))
            alias = client.recv(1024)
            player = Player(alias)
            aliases.append(alias)
            clients.append(client)
            player_objs.append(player)
            print(f'The alias of this client is {alias}'.encode('utf-8'))
            
            thread = threading.Thread(target = handle_client, args=(client, player_id, ))
            thread.start()
        else:
            client.send('Server is full, try again later'.encode('utf-8'))

def broadcast(message):

    for client in clients:
        client.sendall(pickle.dumps(message))

def handle_client(client, player_number):

    while True:
        msg = client.recv(1024)
        key = pickle.loads(msg)

        if key == 115:
            move_down(player_number)
        elif key == 119:
            move_up(player_number)
        elif key == 97:
            move_left(player_number)
        elif key == 100:
            move_right(player_number)
        elif key == 102:
            fireball(player_number, client)

if __name__ == "__main__":
    receive_thread = threading.Thread(target=receive, args=())
    receive_thread.start()

    send_thread = threading.Thread(target=send, args=())
    send_thread.start()