from socket import socket, AF_INET, SOCK_DGRAM, timeout


class CustomSocket:
    __abstract__ = True

    def __init__(
        self, destination_address=None, timeout=5, host="", port=0
    ):
        self.destination_address = destination_address
        self.socket = socket(AF_INET, SOCK_DGRAM)
        self.socket.bind((host, port))
        # Bind to a random port if no port and host are specified
        self.set_timeout(timeout)

    def set_timeout(self, timeout):
        self.socket.settimeout(timeout)

    def send_data(self, message):
        raise NotImplementedError

    def receive(self):
        raise NotImplementedError

    @property
    def port(self):
        return self.socket.getsockname()[1]

    def set_destination_address(self, destination_address):
        self.destination_address = destination_address
