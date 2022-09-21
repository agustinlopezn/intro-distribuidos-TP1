import threading


class FileHandler():
    def __init__(self, socket, client_address):
        super().__init__()
        self.socket = socket
        self.client_address = client_address

    def run(self):
        raise NotImplementedError
