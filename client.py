import threading
import socket
import sys, tty, termios
import pickle
import os
from variables import *


# alias=input('Type alias')

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 59000))

def client_receive():
    while True:
        try:
            msg = client.recv(1024)
            message = pickle.loads(msg)
            os.system('clear')
            print("\r", message, end="")
        except Exception as e:
            pass
        

def client_send():
    while True:
        # message = f'{alias}: {input("")}'
        key = ord(getch())
        client.sendall(pickle.dumps(key))

def getch(char_width=1):
    '''get a fixed number of typed characters from the terminal. 
    Linux / Mac only'''
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        ch = sys.stdin.read(char_width)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

receive_thread = threading.Thread(target=client_receive, args=())
receive_thread.start()

send_thread = threading.Thread(target=client_send, args=())
send_thread.start()
