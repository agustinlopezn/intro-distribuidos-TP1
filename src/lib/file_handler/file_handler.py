import os

from dotenv import load_dotenv
from lib.custom_socket.gbn_socket import GBNSocket
from lib.custom_socket.saw_socket import SaWSocket


load_dotenv()


class FileHandler:
    CHUNK_SIZE = 65536

    def __init__(self, logger, **kwargs):
        socket_type = SaWSocket if os.getenv("SOCKET_TYPE") == "SAW" else GBNSocket
        self.socket = socket_type(logger=logger, **kwargs)
        self.logger = logger
        self.file_name = None  # not necessary, just works as variable declaration
        self.file_size = None  # not necessary, just works as variable declaration
