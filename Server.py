import socket, pickle, _thread

class SERVER:
    DISCONNECT = 0
    PING = 1
    GET = 2

HOST = '127.0.0.1'  
PORT = 65432
SEED = 0

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen()

def client(conn, null):
    while True:
        try:
            data = pickle.loads(conn.recv(2048))
        except EOFError:
            break
        else:
            if data == SERVER.DISCONNECT: break
            elif data == SERVER.PING: conn.send(pickle.dumps("Pong"))

def server():
    pass

_thread.start_new_thread(server, ())

while True:
    conn, addr = s.accept()
    _thread.start_new_thread(client, (conn, 0))

import socket, Modules, pickle
from _thread import *

HOST = '127.0.0.1'  
PORT = 65432
server = Modules.Server()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen()

def threaded(conn, playercount):
    conn.send(pickle.dumps(server))
    while True:
        data = pickle.loads(conn.recv(2048))
        if data == "Stop":
            if name in server.PlayerNames:
                server.RemovePlayer(name)
            break
        else:
            name = data.Name
            server.AddUpdatePlayer(data)
            conn.send(pickle.dumps(server))

while True:
    conn, addr = s.accept()
    start_new_thread(threaded, (conn, 0))
