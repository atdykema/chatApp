import threading
import zlib
import struct
import time
import json
import selectors
import socket as s

from game import *
from server import server_connections, server_settings
from player import *
from map import *
from server_utility import *

def add_new_connection(sock, mask):
    request_connection_packet, client_address_and_port = sock.recvfrom(1024)

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
                if find_existing_client_index([client_address_and_port[0], client_address_and_port[1]]) == -1:
                    print(f'Attempting connection with {str(client_address_and_port)}')
                    
                    client_index = find_free_client_index()

                    server_connections.selector.register(server_connections.PLAYER_SERVER_SOCKETS[client_index], selectors.EVENT_READ, update_server)

                    server_connections.client_address_and_port[client_index] = [client_address_and_port[0], client_address_and_port[1]]
                    server_connections.client_connected[client_index] = True
                    server_connections.connected_clients += 1

                    player = Player(None)

                    server_connections.player_ids[client_index] = player.player_id
                    server_connections.player_objs[player.player_id] = player
                    
                    world_map[player.location[0]][player.location[1]].players[player.player_id] = player

                    print(f'Connected with {str(client_address_and_port)}')
                    print(server_connections.client_address_and_port[client_index],
                          server_connections.client_connected[client_index],
                          server_connections.connected_clients,
                          server_connections.player_ids[client_index],
                          server_connections.player_objs[player.player_id])
                    print(server_connections.client_address_and_port)

                client_index = find_existing_client_index([client_address_and_port[0], client_address_and_port[1]])

                data = f'Connection Accepted:{client_index}:{server_connections.PLAYER_SERVER_PORTS[client_index]}'
                packet = data.encode()
                checksum = zlib.crc32(packet)

                udp_header = struct.pack("!IIII", server_connections.client_address_and_port[client_index][1], server_settings.PLAYER_CONNECTION_SERVER_PORT, len(packet), checksum)

                udp_packet = udp_header + packet

                server_settings.PLAYER_CONNECTION_SERVER_SOCKET.sendto(udp_packet, (client_address_and_port[0], client_address_and_port[1]))

            else:
                data = f'Connection Denied'
                packet = data.encode()
                checksum = zlib.crc32(packet)

                udp_header = struct.pack("!IIII", server_connections.client_address_and_port[client_index][1], server_settings.PLAYER_CONNECTION_SERVER_PORT, len(packet), checksum)

                udp_packet = udp_header + packet

                server_settings.PLAYER_CONNECTION_SERVER_SOCKET.sendto(udp_packet, (client_address_and_port[0], client_address_and_port[1]))


server_connections.selector.register(server_settings.PLAYER_CONNECTION_SERVER_SOCKET, selectors.EVENT_READ, add_new_connection)


def receive():
    print('SERVER READY TO RECEIVE')
    while True:
        for key, mask in server_connections.selector.select():
            callback = key.data
            print("callback: ", callback, "fileobj: ", key.fileobj, "mask: ", mask)
            callback(key.fileobj, mask)
                

def update_clients():
    while True:

        current_world_map = world_map.copy()
        
        for i in range(server_connections.max_clients):
            if server_connections.client_connected[i]:
                world_update = build_viewbox(current_world_map, server_connections.player_objs[server_connections.player_ids[i]])
                
                packet = json.dumps({'world_update':world_update}).encode()
               
                udp_header = struct.pack("!IIII", server_connections.client_address_and_port[i][1], server_connections.PLAYER_SERVER_PORTS[i], len(packet), zlib.crc32(packet))
                
                udp_packet = udp_header + packet

                server_settings.PLAYER_CONNECTION_SERVER_SOCKET.sendto(udp_packet, (server_connections.client_address_and_port[i][0], server_connections.client_address_and_port[i][1]))
        time.sleep(.1)  


def update_server(conn, mask):
    packet, client_address_and_port = conn.recvfrom(1024)
    print("update_clients packet: ", packet)
    print("client_address_and_port:  ", client_address_and_port)

    udp_header = struct.unpack('!IIII', packet[:16])

    print(packet[16:].decode())
    key_and_index = packet[16:].decode().split(':')

    key = int(key_and_index[0])

    index = int(key_and_index[1])

    print("key: ", key)

    print("index: ", index)

    player = server_connections.player_objs[server_connections.player_ids[index]]
    print('moving player: ', player.player_id)
    print(player)
    print(index)
    #checksum

    print("update_server: ", key)
    if key == 113:

        print("server disconnect")
        data = 'You are disconnected'
        packet = data.encode()
        checksum = zlib.crc32(packet)
        udp_header = struct.pack("!IIII", server_connections.client_address_and_port[index][1], server_connections.PLAYER_SERVER_PORTS[index], len(packet), checksum)
        udp_packet = udp_header + packet
        for _ in range(10):
            server_connections.PLAYER_SERVER_SOCKETS[index].sendto(udp_packet, (server_connections.client_address_and_port[index][0], server_connections.client_address_and_port[index][1]))

        del server_connections.player_objs[player.player_id]
        server_connections.client_address_and_port[index] = None
        server_connections.client_connected[index] = False
        server_connections.connected_clients -= 1
        server_connections.player_ids[index] = None
                    
        return
        
    print("current_player_vars: ", vars(player))
    print("player_objs: ", server_connections.player_objs)
    print("player_ids: ", server_connections.player_ids)
    if key == 115:
        move_down(player)
    elif key == 119:
        move_up(player)
    elif key == 97:
        move_left(player)
    elif key == 100:
        move_right(player)
        
def build_viewbox(map_update, player):

    viewbox = [([' '] * ((server_settings.MAX_VIEWBOX[0] * 2 ) - 1)) for i in range((server_settings.MAX_VIEWBOX[1] * 2) - 1)]

    left_most_player_view = (player.location[0] - server_settings.MAX_VIEWBOX[0] if player.location[0] - server_settings.MAX_VIEWBOX[0] > 0 else 0)
    #right_most_player_view = player.location[0] + server_settings.MAX_VIEWBOX[0] if player.location[0] + server_settings.MAX_VIEWBOX[0] < server_settings.MAP_DIMENSIONS[0] else server_settings.MAP_DIMENSIONS[0]

    top_most_player_view = player.location[1] - server_settings.MAX_VIEWBOX[1] if player.location[1] - server_settings.MAX_VIEWBOX[1] > 0 else 0
    #bottom_most_player_view = player.location[1] + server_settings.MAX_VIEWBOX[1] if player.location[1] + server_settings.MAX_VIEWBOX[1] < server_settings.MAP_DIMENSIONS[1] else server_settings.MAP_DIMENSIONS[1]

    for i in range(len(viewbox)):
        vert_pos = top_most_player_view + i
        if vert_pos >= server_settings.MAP_DIMENSIONS[1]:
            continue
        for j in range(len(viewbox[i])):
            horiz_pos = left_most_player_view + j
            if horiz_pos >= server_settings.MAP_DIMENSIONS[0]:
                continue
            if map_update[horiz_pos][vert_pos].players:
                if player.player_id in map_update[horiz_pos][vert_pos].players:
                    viewbox[i][j] = player.my_indicator
                else:
                    #print("horzi: ", horiz_pos, "vert: ", vert_pos, map_update[horiz_pos][vert_pos].tile_id, map_update[horiz_pos][vert_pos].players)
                    viewbox[i][j] = list(map_update[horiz_pos][vert_pos].players.values())[0].indicator
            else:
                viewbox[i][j] = map_update[horiz_pos][vert_pos].properties.tile_texture 
    
    return viewbox
