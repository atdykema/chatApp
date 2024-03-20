from server import server_connections

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