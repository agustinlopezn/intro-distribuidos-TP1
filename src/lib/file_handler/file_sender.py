from lib.protocol_handler import OperationCodes
from .file_handler import FileHandler
import os

class FileSender(FileHandler):
    def __init__(self, socket, client_address, source_folder):
        self.source_folder = source_folder
        super().__init__(socket, client_address)

    def send_file(self, file_name):
        with open(f"{self.source_folder}/{file_name}", "rb") as file:
            bytes_sent = 0
            while True:
                data = file.read(512)
                if not data:
                    break
                try:
                    self.socket.send_data(data)
                    bytes_sent += len(data)
                except Exception as e:
                    print(e)
                    break
            return bytes_sent

    def get_file_size(self, file_name):
        return os.stat(f"{self.source_folder}/{file_name}").st_size

