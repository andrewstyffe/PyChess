import socket
from _thread import *
import sys


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server = 'localhost'
port = 5555

server_ip = socket.gethostbyname(server)

try:
    s.bind((server, port))

except socket.error as e:
    print(str(e))

s.listen(2)
print("Waiting for a connection")

global num_clients
num_clients = 0
def threaded_client(our_conn, opponents_conn, colour):
    our_conn.send(str.encode(colour))
    while True:
        try:
            move = our_conn.recv(2048).decode()
            print(move)
            if not move:
                our_conn.send(str.encode("Goodbye"))
                break
            else:
                print("Recieved: " + move)
                print(f"Sending {move} to opponent.")
                opponents_conn.send(str.encode(move))
        except Exception as e:
            print(str(e))

    print("Connection Closed")
    conn.close()

white_conn = None
black_conn = None
white_addr = None
black_addr = None
while num_clients != 2:
    conn, addr = s.accept()
    print("Connected to: ", addr)
    num_clients += 1

    if num_clients == 1:
        white_conn = conn
        white_addr = addr
    elif num_clients == 2:
        black_conn = conn
        black_addr = addr

# Create a thread for each player's socket.
start_new_thread(threaded_client, (white_conn, black_conn, 'white',))
start_new_thread(threaded_client, (black_conn, white_conn, 'black',))

while True:
    pass