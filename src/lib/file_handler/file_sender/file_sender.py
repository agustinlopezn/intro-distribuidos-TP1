import os
from src.lib.file_handler.file_handler import FileHandler
import time


class FileSender(FileHandler):
    __abstract__ = True

    def __init__(self, src_folder, **kwargs):
        super().__init__(**kwargs)
        self.source_folder = src_folder

    def handle_send_process(self):
        self._handle_send_process()


    def send_file(self, showProgress=True):
        self.logger.debug(f"Sending {self.file_name}")
        try:
            with open(f"{self.source_folder}/{self.file_name}", "rb") as file:
                bytes_sent = 0
                while bytes_sent < self.file_size:
                    data = file.read(self.CHUNK_SIZE)
                    self.logger.debug("Sending data...")
                    self.socket.send_data(data)
                    bytes_sent += len(data)
                    self.logger.info(
                        f"Progress: {bytes_sent/self.file_size * 100:.0f}%"
                    )
                return
        except Exception as e:
            self.logger.error("There was an error while sending the file")
                

    def get_file_size(self, file_name):
        return os.stat(f"{self.source_folder}/{file_name}").st_size
