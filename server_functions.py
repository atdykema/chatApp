import threading
import zlib
import struct
import time
import json

from game import *
from server import server_connections, server_settings
from player import *
from map import *

def find_free_client_index():
    for i in range(server_connections.max_clients):
        if server_connections.client_connected[i]:
            return i
    return -1

def find_existing_client_index(address):
    for i in range(server_connections.max_clients):
        if server_connections.client_connected[i] and server_connections.client_address[i] == address:
            return i
    return -1

def is_cliented_connected(client_index):
    return server_connections.client_connected[client_index]

def get_client_address(client_index):
    return server_connections.client_address[client_index]


def receive():
    print('SERVER READY TO RECEIVE')
    while True:
        request_connection_packet, client_address_and_port = server_settings.PLAYER_CONNECTION_SERVER_SOCKET.recvfrom(1024)

        print("request_connection_packet: ", request_connection_packet)

        print("address: ", client_address_and_port)

        udp_header = struct.unpack("!IIII", request_connection_packet[:16])

        print(udp_header)

        packet_data = request_connection_packet[16:]

        correct_checksum = udp_header[3]

        current_checksum = zlib.crc32(packet_data)

        message = packet_data.decode()

        print(message)
        
        if correct_checksum == current_checksum and message == 'Connection Request':
            if server_connections.connected_clients < server_settings.MAX_PLAYERS:
                if find_existing_client_index(client_address_and_port[0]) == -1:
                    print(f'Attempting connection with {str(client_address_and_port)}')
                    
                    client_index = find_free_client_index()

                    server_connections.client_address[client_index] = client_address_and_port[0]
                    server_connections.client_port[client_index] = client_address_and_port[1]
                    server_connections.client_connected[client_index] = True
                    server_connections.connected_clients += 1

                    player = Player(None) #replace with getting player from database

                    server_connections.player_ids[client_index] = player.player_id
                    server_connections.player_objs[player.player_id] = player
                    
                    world_map[player.location[0]][player.location[1]].players.add(player.player_id)

                    update_server_thread = threading.Thread(target = update_server, args=(client_index, ))
                    update_server_thread.start()

                    print(f'Connected with {str(client_address_and_port)}')

                client_index = find_existing_client_index(client_address_and_port[0])

                data = f'Connection Accepted:{client_index}:{server_connections.PLAYER_SERVER_PORTS[client_index]}'
                packet = data.encode()
                checksum = zlib.crc32(packet)

                udp_header = struct.pack("!IIII", server_connections.client_port[client_index], server_settings.PLAYER_CONNECTION_SERVER_PORT, len(packet), checksum)

                udp_packet = udp_header + packet

                server_settings.PLAYER_CONNECTION_SERVER_SOCKET.sendto(udp_packet, (client_address_and_port[0], client_address_and_port[1]))

            else:
                data = f'Connection Denied'
                packet = data.encode()
                checksum = zlib.crc32(packet)

                udp_header = struct.pack("!IIII", server_connections.client_port[client_index], server_settings.PLAYER_CONNECTION_SERVER_PORT, len(packet), checksum)

                udp_packet = udp_header + packet

                server_settings.PLAYER_CONNECTION_SERVER_SOCKET.sendto(udp_packet, (client_address_and_port[0], client_address_and_port[1]))

        

def update_clients():
    while True:

        current_world_map = world_map.copy()
        
        for i in range(server_connections.max_clients):
            if server_connections.client_connected[i]:
                world_update = build_viewbox(current_world_map, server_connections.player_objs[server_connections.player_ids[i]])
                
                packet = json.dumps({'world_update':world_update}).encode()
               
                udp_header = struct.pack("!IIII", server_connections.client_port[i], server_connections.PLAYER_SERVER_PORTS[i], len(packet), zlib.crc32(packet))
                
                udp_packet = udp_header + packet

                print(udp_packet)

                server_settings.PLAYER_CONNECTION_SERVER_SOCKET.sendto(udp_packet, (server_connections.client_address[i], server_connections.client_port[i]))
        time.sleep(.02)


def update_server(index):

    player = server_connections.player_objs[server_connections.player_ids[index]]

    while True:
        packet = server_connections.PLAYER_SERVER_SOCKETS[index].recv(1024)
        #checksum
        udp_header = struct.unpack('!IIII', packet[:16])

        key = int(packet[16:])
        print("update_server: ", key)
        if key == 113:

            print("server disconnect")
            data = 'You are disconnected'
            packet = data.encode()
            checksum = zlib.crc32(packet)
            udp_header = struct.pack("!IIII", server_connections.client_port[index], server_connections.PLAYER_SERVER_PORTS[index], len(packet), checksum)
            udp_packet = udp_header + packet
            for _ in range(10):
                server_connections.PLAYER_SERVER_SOCKETS[index].sendto(udp_packet, (server_connections.client_address[index], server_connections.client_port[index]))

            del server_connections.player_objs[player.player_id]
            server_connections.client_address[index] = None
            server_connections.client_port[index] = None
            server_connections.client_connected[index] = False
            server_connections.connected_clients -= 1
            server_connections.player_ids[index] = None
                        
            return
        if key == 115:
            move_down(player)
        elif key == 119:
            move_up(player)
        elif key == 97:
            move_left(player)
        elif key == 100:
            move_right(player)
        
def build_viewbox(map_update, player):

    viewbox = [([None] * ((server_settings.MAX_VIEWBOX[0] * 2 ) - 1)) for i in range((server_settings.MAX_VIEWBOX[1] * 2) - 1)]

    left_most_player_view = (player.location[0] - server_settings.MAX_VIEWBOX[0] if player.location[0] - server_settings.MAX_VIEWBOX[0] > 0 else 0)
    right_most_player_view = player.location[0] + server_settings.MAX_VIEWBOX[0] if player.location[0] + server_settings.MAX_VIEWBOX[0] < server_settings.MAP_DIMENSIONS[0] else server_settings.MAP_DIMENSIONS[0]

    top_most_player_view = player.location[1] - server_settings.MAX_VIEWBOX[1] if player.location[1] - server_settings.MAX_VIEWBOX[1] > 0 else 0
    bottom_most_player_view = player.location[1] + server_settings.MAX_VIEWBOX[1] if player.location[1] + server_settings.MAX_VIEWBOX[1] < server_settings.MAP_DIMENSIONS[1] else server_settings.MAP_DIMENSIONS[1]

    for i in range(len(viewbox)):
        vert_pos = top_most_player_view + i
        if vert_pos > server_settings.MAP_DIMENSIONS[1]:
            continue
        for j in range(len(viewbox[i])):
            horiz_pos = left_most_player_view + j
            if horiz_pos > server_settings.MAP_DIMENSIONS[0]:
                continue
            if player.location == [horiz_pos, vert_pos]:
                viewbox[i][j] = player.indicator
            else:
                viewbox[i][j] = map_update[horiz_pos][vert_pos].properties.tile_texture
    
    return viewbox
