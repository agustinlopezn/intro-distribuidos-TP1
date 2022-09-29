from socket import socket, AF_INET, SOCK_DGRAM, timeout
from lib.logger import Logger


class CustomSocket:
    __abstract__ = True

    def __init__(self, opposite_address=None, timeout=5, host="", port=0, logger=None):
        self.opposite_address = opposite_address
        self.socket = socket(AF_INET, SOCK_DGRAM)
        self.socket.bind((host, port))
        # Bind to a random port if no port and host are specified
        self.set_timeout(timeout)
        self.logger = logger

    def set_timeout(self, timeout):
        self.socket.settimeout(timeout)

    def send_data(self, message):
        raise NotImplementedError

    def receive(self):
        raise NotImplementedError

    def send_dl_request(self):
        raise NotImplementedError

    @property
    def port(self):
        return self.socket.getsockname()[1]
