import socket


class Network:

    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = "127.0.0.1"
        self.port = 5555
        self.addr = (self.host, self.port)
        self.id = self.connect()

    def connect(self):
        self.client.connect(self.addr)
        reply = self.client.recv(2048) 
        return reply

    def send(self, chess_move):
        try:
            self.client.send(str.encode(chess_move))
            reply = self.client.recv(2048).decode()
            return reply
        except socket.error as e:
            return str(e)