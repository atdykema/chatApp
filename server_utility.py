from server import server_connections
import zlib
import struct
import json

def find_free_client_index():
    for i in range(server_connections.max_clients):
        if not server_connections.client_connected[i]:
            return i
    return -1

def find_existing_client_index(address_and_port):
    for i in range(server_connections.max_clients):
        if server_connections.client_connected[i] and server_connections.client_address_and_port[i] == address_and_port:
            return i
    return -1

def is_cliented_connected(client_index):
    return server_connections.client_connected[client_index]

def get_client_address_and_port(client_index):
    return server_connections.client_address_and_port[client_index]

def create_packet(message, client_port, server_port):

    message = message.encode()

    checksum = zlib.crc32(message)

    udp_header = struct.pack("!IIII", client_port, server_port, len(message), checksum)

    return udp_header + message


def create_json_packet(message, client_port, server_port):

    packet = json.dumps({'message':message}).encode()
               
    udp_header = struct.pack("!IIII", client_port, server_port, len(packet), zlib.crc32(packet))
    
    return udp_header + packet


def extract_packet(packet):

    udp_header = struct.unpack("!IIII", packet[:16])

    message = packet[16:]

    correct_checksum = udp_header[3]

    current_checksum = zlib.crc32(message)

    message = message.decode()

    return message, udp_header, correct_checksum, current_checksum