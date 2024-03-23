import socket as s

CLIENT_PORT = 58999
SERVER_PORT = 59000

CLIENT_ADDRESS = '127.0.0.1'
SERVER_ADDRESS = '127.0.0.1'

MAX_VIEWBOX = [5, 5]

client_not_bound = True

while client_not_bound:
    client_socket = s.socket(s.AF_INET, s.SOCK_DGRAM)
    try:
        client_socket.bind((CLIENT_ADDRESS, CLIENT_PORT))
        client_not_bound = False
    except:
        CLIENT_PORT -= 1

class ClientState():
    DISCONNECTED = 'disconnected'
    CONNECTING = 'connecting'
    CONNECTED = 'connected'

client_state = ClientState.DISCONNECTED

class ClientSettings():
    def __init__(self):
        self.client_state = client_state
        self.assigned_server_port = None
        self.index = None
        self.client_socket = client_socket
        self.CLIENT_PORT = CLIENT_PORT
        self.SERVER_PORT = SERVER_PORT
        self.CLIENT_ADDRESS = CLIENT_ADDRESS
        self.SERVER_ADDRESS = SERVER_ADDRESS
        self.MAX_VIEWBOX = MAX_VIEWBOX
        self.update = None

client_settings = ClientSettings()