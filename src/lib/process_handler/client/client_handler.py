from threading import Thread

class ClientHandler():
    __abstract__ = True
    
    def __init__(self, socket, destination_address):
        super().__init__()
        self.socket = socket
        self.destination_address = destination_address