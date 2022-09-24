from lib.protocol_handler import OperationCodes
from .file_handler import FileHandler

import os.path

class FileReceiver(FileHandler):
    def __init__(self, socket, client_address, destination_folder):
        self.destination_folder = destination_folder
        super().__init__(socket, client_address)

    def get_valid_name(self, file_name):
        counter = 1
        name_parts = os.path.splitext(file_name)
        while os.path.exists(file_name):
            file_name = name_parts[0] + (f" ({counter})" + name_parts[1])
            counter += 1
        return file_name

    def receive_file(self, file_name, file_size, showProgress=False):
        file_name = self.get_valid_name(f"{self.destination_folder}/{file_name}")

        with open(file_name, "wb") as f:
            bytes_received = 0
            while bytes_received < file_size:
                data = self.socket.receive_data()
                f.write(data)
                bytes_received += len(data)
                if showProgress:
                    print(f"Progress: {bytes_received/file_size * 100:.0f}%", end='\r')
            print("")
            return bytes_received
