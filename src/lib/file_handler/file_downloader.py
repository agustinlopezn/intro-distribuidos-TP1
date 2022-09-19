from lib.protocol_handler import OperationCodes
from .file_handler import FileHandler


class FileDownloader(FileHandler):
    def __init__(self, socket, client_address):
        super().__init__(socket, client_address)

    def run(self):
        msg, client_address = self.socket.receive()
        print(msg)
        
            