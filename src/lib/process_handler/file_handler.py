import threading

from lib.custom_socket.saw_socket import SaWSocket
from lib.logger import Logger


class FileHandler:
    CHUNK_SIZE = 2048

    def __init__(self, opposite_address, host="", port=0):
        super().__init__()
        self.socket = SaWSocket(
            opposite_address=opposite_address, timeout=3, host=host, port=port
        )
        self.opposite_address = opposite_address
        self.logger = Logger(self.__class__.__name__)
        self.file_name = None  # not necessary, just works as variable declaration
        self.file_size = None  # not necessary, just works as variable declaration
