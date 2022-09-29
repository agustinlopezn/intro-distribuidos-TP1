import threading
from lib.custom_socket.gbn_socket import GBNSocket
from lib.custom_socket.saw_socket import SaWSocket
from lib.logger import Logger


class FileHandler:
    CHUNK_SIZE = 2048

    def __init__(self, opposite_address, logger, host="", port=0):
        super().__init__()
        self.socket = GBNSocket(
            opposite_address=opposite_address,
            timeout=3,
            host=host,
            port=port,
            logger=logger,
        )
        self.opposite_address = opposite_address
        self.logger = logger
        self.file_name = None  # not necessary, just works as variable declaration
        self.file_size = None  # not necessary, just works as variable declaration
