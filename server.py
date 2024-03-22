import socket as s
import selectors

MAX_PLAYERS = 10
PLAYER_CONNECTION_SERVER_PORT = 59000
SERVER_ADDRESS = "127.0.0.1"
PLAYER_SPAWN = [1, 1]
MAP_DIMENSIONS = [-1, -1]
MAX_VIEWBOX = [5, 5]
TICK_RATE = 1/10

player_request_connection_socket = s.socket(s.AF_INET, s.SOCK_DGRAM)
player_request_connection_socket.setblocking(False)
player_request_connection_socket.bind((SERVER_ADDRESS, PLAYER_CONNECTION_SERVER_PORT))

selector = selectors.DefaultSelector()

PLAYER_CONNECTION_PORTS = []

for i in range(MAX_PLAYERS):
    PLAYER_CONNECTION_PORTS.append(PLAYER_CONNECTION_SERVER_PORT + i + 1)
print(PLAYER_CONNECTION_PORTS)

class Server:
    def __init__(self):
        self.max_clients = MAX_PLAYERS
        self.connected_clients = 0
        self.player_ids = [None] * MAX_PLAYERS
        self.player_objs = dict()
        self.client_connected = [False] * MAX_PLAYERS
        self.client_address_and_port = [None] * MAX_PLAYERS
        self.player_connection_sockets = [None] * MAX_PLAYERS #array of sockets for player clients
        self.PLAYER_CONNECTION_PORTS = PLAYER_CONNECTION_PORTS #array of ports for player clients
        self.selector = selector
    
class ServerSettings():
    def __init__(self):
        self.SERVER_ADDRESS = SERVER_ADDRESS
        self.PLAYER_CONNECTION_SERVER_PORT = PLAYER_CONNECTION_SERVER_PORT
        self.PLAYER_SPAWN = PLAYER_SPAWN
        self.MAX_PLAYERS = MAX_PLAYERS
        self.MAP_DIMENSIONS = MAP_DIMENSIONS
        self.MAX_VIEWBOX = MAX_VIEWBOX
        self.PLAYER_CONNECTION_SERVER_SOCKET = player_request_connection_socket #inital port used to get assigned port
        self.TICK_RATE = TICK_RATE

server_connections = Server()

server_settings = ServerSettings()