import threading

from lib.custom_socket.saw_socket import SaWSocket

class FileHandler():
    CHUNK_SIZE = 2048
    
    def __init__(self, opposite_address):
        super().__init__()
        self.socket = SaWSocket(opposite_address=opposite_address, timeout=3)
        self.opposite_address = opposite_address
        self.file_name = None # not necessary, just works as variable declaration
        self.file_size = None # not necessary, just works as variable declaration
