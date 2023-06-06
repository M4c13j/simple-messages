import socket
import sys

HOST = "127.0.0.1"
PORT = 65456

server = socket.socket(
    socket.AF_INET,
    socket.SOCK_STREAM
)

server.connect( (HOST, PORT) )
server.sendall(b"Penis Kutas siurrrr")
data = server.recv(1024)

print(f"Recieved {data}")