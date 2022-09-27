import os
from threading import Thread

from lib.process_handler.file_handler import FileHandler


class FileSender(FileHandler):
    __abstract__ = True

    def __init__(self, opposite_address, src_folder):
        super().__init__(opposite_address)
        self.source_folder = src_folder

    def handle_send_process(self):
        raise NotImplementedError

    def send_file(self, showProgress=True):
        print(f"Sending {self.file_name}")
        with open(f"{self.source_folder}/{self.file_name}", "rb") as file:
            bytes_sent = 0
            while bytes_sent < self.file_size:
                data = file.read(self.CHUNK_SIZE)
                try:
                    print("Sending data...")
                    self.socket.send_data(data)
                    bytes_sent += len(data)
                    print(f"Progress: {bytes_sent/self.file_size * 100:.0f}%")
                except Exception as e:
                    print(e)
                    print(f"Progress: {bytes_sent/self.file_size * 100:.0f}%")
                    break
            print("")
            return bytes_sent

    def get_file_size(self, file_name):
        return os.stat(f"{self.source_folder}/{file_name}").st_size
