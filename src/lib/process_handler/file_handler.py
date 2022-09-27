import threading

class FileHandler():
    CHUNK_SIZE = 2048
    
    def __init__(self, socket, opposite_address):
        super().__init__()
        self.socket = socket
        self.opposite_address = opposite_address
