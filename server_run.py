from server_functions import *

receive_thread = threading.Thread(target=receive, args=())
receive_thread.start()

send_thread = threading.Thread(target=update_clients, args=())
send_thread.start()