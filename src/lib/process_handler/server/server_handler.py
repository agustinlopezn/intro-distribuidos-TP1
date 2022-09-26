from threading import Thread

class ServerHandler(Thread):
    __abstract__ = True
    
    def __init__(self, socket, opposite_address):
        super().__init__()
        self.socket = socket
        self.opposite_address = opposite_address
    