import socket
import sys
import threading
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
print(f"Started server ({HOST},{PORT}) \n Start time: {server_start_time}")

list_of_clients = [] #
nicknames = {}

def userId( conn ):
    # user id is a hash of ip and port 
    return hash( (conn.getpeername()[0],conn.getpeername()[1]) )

# handle server log messages
def server_log(msg):
    print(f"[SERVER] {msg}")

# post messages from clients to chat
def postMessage(msg, conn):
    return f"<{nicknames[userId(conn)]}> {msg}"

def broadcast(msg,conn):
    msg = msg.encode()
    for client in list_of_clients:
        if client != conn:
            client.sendall( msg )

def handle_client(conn: socket.socket):
    while True:
        try:
            msg = conn.recv(1024).decode()
        except:
            remove(conn)
            break

        if msg.startswith("NICKCHANGE"):
            nicknames[userId(conn)] = msg[10:]
            server_log("Nickname changed to"+nicknames[userId(conn)])
            broadcast("Nickname changed to"+nicknames[userId(conn)], None)
            continue
        else:
            tosend = postMessage(msg, conn)
            broadcast( tosend, conn )

    server_log("thread is dead")

def remove(conn):
    if conn in list_of_clients:
        del nicknames[userId(conn)]
        list_of_clients.remove(conn)
    server_log(f"Client {conn.getpeername()} got REMOVED.")
    broadcast( f"Client {conn.getpeername()} has left.", conn )

def run_server():
    server_log("Everything works so far, lets talk.")
    try:
        while True:
            conn, addr = server.accept()
            list_of_clients.append( conn )
            server_log(f"Connection from {addr[0]}, {addr[1]}")
            
            nicknames[userId(conn)] = str(conn.getpeername()[0]) # temporary first name
            broadcast(f"{nicknames[userId(conn)]} has just joined", None)
            NewThread = threading.Thread( target=handle_client, args=(conn,))
            NewThread.daemon = True
            NewThread.start()
    except KeyboardInterrupt:
        exit()

if __name__ == "__main__":
    run_server()
