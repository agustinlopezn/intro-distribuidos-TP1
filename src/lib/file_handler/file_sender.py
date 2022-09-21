from lib.protocol_handler import OperationCodes
from .file_handler import FileHandler
import os

SRC_FOLDER = "../files/downloaded"


class FileSender(FileHandler):
    def __init__(self, socket, client_address, source_folder):
        self.source_folder = source_folder
        super().__init__(socket, client_address)

    def send_file(self, file_name):
        with open(f"{self.source_folder}/{file_name}", "rb") as file:
            while True:
                data = file.read(512)
                try:
                    self.socket.send_data(data)
                except Exception as e:
                    print(e)
                    break
                if not data:
                    break
            self.socket.send_end()
            self.socket.socket.close()
            print("Data sent successfully")

    def get_file_size(self, file_name):
        return os.stat(f"{self.source_folder}/{file_name}").st_size

