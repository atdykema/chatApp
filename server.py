import threading
import socket
import pickle
from game import *
from variables import *
from player import *

host = "127.0.0.1"
port = 59000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind((host, port))

server.listen()

def receive():
    print('SERVER READY TO RECEIVE')
    while True:
        client, address = server.accept()

        if len(clients) < MAX_PLAYERS:
            print(f'connection is established with {str(address)}')
            client.send('alias?: '.encode('utf-8'))
            alias = client.recv(1024)
            player = Player(alias)
            clients[player.player_id] = client
            player_objs[player.player_id] = player
            world_map[player.location[0]][player.location[1]].players.add(player.player_id)
            print(f'The alias of this client is {alias}'.encode('utf-8'))

            update_server_thread = threading.Thread(target = update_server, args=(player.player_id, ))
            update_server_thread.start()

            update_client_thread = threading.Thread(target= update_client, args=(player.player_id, ))
            update_client_thread.start()

        else:
            client.send('Server is full, try again later'.encode('utf-8'))

def update_client(player_id):
    while True:
        if clients.get(player_id) is None:
            print(f"{player_id} has disconnected")
            return
        
        current_world_map = world_map.copy()

        world_update = build_map(current_world_map, player_objs[player_id])

        clients[player_id].sendall(pickle.dumps(world_update))

def update_server(player_id):

    client = clients[player_id]
    player = player_objs[player_id]

    while True:
        msg = client.recv(1024)
        key = pickle.loads(msg)

        if key == 113:
            client.close()
            del clients[player_id]
            del player_objs[player_id]
            return
        elif key == 115:
            move_down(player)
        elif key == 119:
            move_up(player)
        elif key == 97:
            move_left(player)
        elif key == 100:
            move_right(player)
        elif key == 102:
            fireball(player)

def build_map(map_update, player):

    viewbox = [([None] * ((MAX_VIEWBOX[0] * 2 ) - 1)) for i in range((MAX_VIEWBOX[1] * 2) - 1)]

    left_most_player_view = (player.location[0] - MAX_VIEWBOX[0] if player.location[0] - MAX_VIEWBOX[0] > 0 else 0)
    right_most_player_view = player.location[0] + MAX_VIEWBOX[0] if player.location[0] + MAX_VIEWBOX[0] < MAP_DIMENSIONS[0] else MAP_DIMENSIONS[0]

    top_most_player_view = player.location[1] - MAX_VIEWBOX[1] if player.location[1] - MAX_VIEWBOX[1] > 0 else 0
    bottom_most_player_view = player.location[1] + MAX_VIEWBOX[1] if player.location[1] + MAX_VIEWBOX[1] < MAP_DIMENSIONS[1] else MAP_DIMENSIONS[1]

    for i in range(len(viewbox)):
        vert_pos = top_most_player_view + i
        if vert_pos > MAP_DIMENSIONS[1]:
            continue
        for j in range(len(viewbox[i])):
            horiz_pos = left_most_player_view + j
            if horiz_pos > MAP_DIMENSIONS[0]:
                continue
            if player.location == [horiz_pos, vert_pos]:
                viewbox[i][j] = player.indicator
            else:
                viewbox[i][j] = map_update[horiz_pos][vert_pos].properties.tile_texture
    
    return viewbox

if __name__ == "__main__":
    receive_thread = threading.Thread(target=receive, args=())
    receive_thread.start()