import socket


class CustomSocket:
    __abstract__ = True

    def __init__(self, client_address):
        self.client_address = client_address
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind(("", 0)) # Bind to a random port

    def send(self, message):
        self.socket.sendto(message, self.client_address)

    def receive(self):
        return self.socket.recvfrom(512)

    @property
    def port(self):
        return self.socket.getsockname()[1]
