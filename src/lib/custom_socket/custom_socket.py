from socket import socket, AF_INET, SOCK_DGRAM, timeout


class CustomSocket:
    __abstract__ = True

    def __init__(
        self, opposite_address=None, packet_type=None, timeout=5, host="", port=0
    ):
        self.opposite_address = opposite_address
        self.packet_type = packet_type
        self.socket = socket(AF_INET, SOCK_DGRAM)
        self.socket.bind((host, port))
        # Bind to a random port if no port and host are specified
        self.socket.settimeout(timeout)

    def send_data(self, message):
        raise NotImplementedError

    def receive(self):
        raise NotImplementedError

    @property
    def port(self):
        return self.socket.getsockname()[1]

    def set_opposite_address(self, opposite_address):
        self.opposite_address = opposite_address
