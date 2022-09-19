from socket import socket, AF_INET, SOCK_DGRAM, timeout


class CustomSocket:
    __abstract__ = True

    def __init__(self, client_address, packet_type):
        self.client_address = client_address
        self.packet_type = packet_type
        self.socket = socket(AF_INET, SOCK_DGRAM)
        self.socket.bind(("", 0))  # Bind to a random port
        self.socket.settimeout(2)

    def send(self, message):
        raise NotImplementedError

    def receive(self):
        raise NotImplementedError

    @property
    def port(self):
        return self.socket.getsockname()[1]
