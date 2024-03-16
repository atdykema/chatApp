import socket as s

MAX_PLAYERS = 10
PLAYER_CONNECTION_SERVER_PORT = 59000
SERVER_ADDRESS = "127.0.0.1"
PLAYER_SPAWN = [1, 1]
MAP_DIMENSIONS = [4, 4]
MAX_VIEWBOX = [3, 3]

player_request_connection_socket = s.socket(s.AF_INET, s.SOCK_DGRAM)
player_request_connection_socket.bind((SERVER_ADDRESS, PLAYER_CONNECTION_SERVER_PORT))

player_connection_ports = []
player_connection_sockets = []

for i in range(MAX_PLAYERS):
    player_socket = s.socket(s.AF_INET, s.SOCK_DGRAM)
    player_socket_port = PLAYER_CONNECTION_SERVER_PORT + i + 1
    player_socket.bind((SERVER_ADDRESS, player_socket_port))
    player_connection_ports.append(player_socket_port)
    player_connection_sockets.append(player_socket)


class Server:
    def __init__(self):
        self.max_clients = MAX_PLAYERS
        self.connected_clients = 0
        self.player_ids = [None] * MAX_PLAYERS
        self.player_objs = {}
        self.client_connected = [False] * MAX_PLAYERS
        self.client_address = [None] * MAX_PLAYERS
        self.client_port = [None] * MAX_PLAYERS
        self.PLAYER_SERVER_SOCKETS = player_connection_sockets #array of sockets for player clients
        self.PLAYER_SERVER_PORTS = player_connection_ports #array of ports for player clients
    
class ServerSettings():
    def __init__(self):
        self.SERVER_ADDRESS = SERVER_ADDRESS
        self.PLAYER_CONNECTION_SERVER_PORT = PLAYER_CONNECTION_SERVER_PORT
        self.PLAYER_SPAWN = PLAYER_SPAWN
        self.MAX_PLAYERS = MAX_PLAYERS
        self.MAP_DIMENSIONS = MAP_DIMENSIONS
        self.MAX_VIEWBOX = MAX_VIEWBOX
        self.PLAYER_CONNECTION_SERVER_SOCKET = player_request_connection_socket #inital port used to get assigned port

server_connections = Server()

server_settings = ServerSettings()