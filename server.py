import socket
import sys
import _thread
import time

HOST = "127.0.0.1"
PORT = 65456

server = socket.socket(
    socket.AF_INET,
    socket.SOCK_STREAM
)

server.bind( (HOST, PORT) )
server.listen()
server_start_time = time.strftime("%X %x")
print(f"Started server ({HOST},{PORT})   time: {server_start_time}")

list_of_clients = []

def handle_client(conn):
    conn.send("Sup bro")

    while True:
        try:
            msg = conn.recv(1024)
            if msg:
                print(f"<{conn.getpeername()[0]}>: {msg}")
            else:
                remove(conn)
        except:
            continue

def remove(conn):
    if conn in list_of_clients:
        list_of_clients.remove(conn)
    print(f"Client {conn.getpeername()} got removed.")

def run_server():
    while True:
        conn, addr = server.accept()
        list_of_clients.append(conn)
        print(f"Connection from {addr[0]}, {addr[1]}")
        _thread.start_new_thread( handle_client, (conn,))

if __name__ == "__main__":
    run_server()
