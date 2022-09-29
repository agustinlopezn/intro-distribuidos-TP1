import os
from threading import Thread
from src.lib.custom_socket.saw_socket import SaWSocket
from src.lib.process_handler.file_handler import FileHandler


class FileReceiver(FileHandler):
    def __init__(self, opposite_address, dest_folder, logger, host="", port=0):
        self.destination_folder = dest_folder
        super().__init__(
            opposite_address=opposite_address, host=host, port=port, logger=logger
        )

    def get_valid_name(self, file_name):
        counter = 1
        name_parts = os.path.splitext(file_name)
        while os.path.exists(file_name):
            file_name = name_parts[0] + (f" ({counter})" + name_parts[1])
            counter += 1
        return file_name

    def handle_receive_process(self):
        raise NotImplementedError

    def receive_file(self, showProgress=True):
        file_name = self.get_valid_name(f"{self.destination_folder}/{self.file_name}")
        with open(file_name, "wb") as f:
            bytes_received = 0
            while bytes_received < self.file_size:
                data = self.socket.receive_data()
                f.write(data)
                bytes_received += len(data)
                print(f"Progress: {bytes_received/self.file_size * 100:.0f}%")
            print("")
            return bytes_received
