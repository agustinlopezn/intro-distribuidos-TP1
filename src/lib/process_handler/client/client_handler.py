from threading import Thread

class ClientHandler():
    __abstract__ = True
    
    def __init__(self, socket, oposite_address):
        super().__init__()
        self.socket = socket
        self.oposite_address = oposite_address