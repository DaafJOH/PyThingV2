import socket, pickle, time

HOST = '127.0.0.1'  
PORT = 65432

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
ping = pickle.dumps(1)
t = time.perf_counter()
s.send(ping)
res = s.recv(2048)
t2 = time.perf_counter()
print(int((t2-t)*1000))
print("great!")