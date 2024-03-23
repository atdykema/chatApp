import zlib
import struct
import json

from client import client_settings

def create_packet(message, port):

    message = message.encode()

    checksum = zlib.crc32(message)

    udp_header = struct.pack("!IIII", client_settings.CLIENT_PORT, port, len(message), checksum)

    return udp_header + message


def extract_packet(packet):

    udp_header = struct.unpack("!IIII", packet[:16])

    message = packet[16:]

    correct_checksum = udp_header[3]

    current_checksum = zlib.crc32(message)

    message = message.decode()

    return message, udp_header, correct_checksum, current_checksum