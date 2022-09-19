import socket


class CustomSocket:
    __abstract__ = True

    def __init__(self, client_address):
        self.client_address = client_address
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def send(self, message):
        self.socket.sendto(message, self.client_address)

    def receive(self):
        pass
