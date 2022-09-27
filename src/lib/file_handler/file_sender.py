from lib.protocol_handler import OperationCodes
from .file_handler import FileHandler
import os


class FileSender(FileHandler):
    def __init__(self, socket, client_address, source_folder):
        self.source_folder = source_folder
        super().__init__(socket, client_address)

    def send_file(self, file_name, file_size, showProgress=False):
        print(f"Sending {file_name}")
        with open(f"{self.source_folder}/{file_name}", "rb") as file:
            bytes_sent = 0
            while bytes_sent < file_size:
                data = file.read(self.CHUNK_SIZE)
                try:
                    print("Sending data...")
                    self.socket.send_data(data)
                    bytes_sent += len(data)
                    print(f"Progress: {bytes_sent/file_size * 100:.0f}%")
                except Exception as e:
                    print(e)
                    print(f"Progress: {bytes_sent/file_size * 100:.0f}%")
                    break
            print("")
            return bytes_sent

    def get_file_size(self, file_name):
        return os.stat(f"{self.source_folder}/{file_name}").st_size

