import threading
from src.lib.custom_socket.gbn_socket import GBNSocket
from src.lib.custom_socket.saw_socket import SaWSocket
from src.lib.logger import Logger


class FileHandler:
    CHUNK_SIZE = 65536

    def __init__(self, opposite_address, logger, host="", port=0):
        super().__init__()
        self.socket = SaWSocket(
            opposite_address=opposite_address,
            host=host,
            port=port,
            logger=logger,
        )
        self.opposite_address = opposite_address
        self.logger = logger
        self.file_name = None  # not necessary, just works as variable declaration
        self.file_size = None  # not necessary, just works as variable declaration
