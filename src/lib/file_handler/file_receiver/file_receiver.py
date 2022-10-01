import os
from threading import Thread
from src.lib.custom_socket.saw_socket import SaWSocket
from src.lib.file_handler.file_handler import FileHandler
import time


class FileReceiver(FileHandler):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def get_valid_name(self, file_name):
        counter = 1
        name_parts = os.path.splitext(file_name)
        while os.path.exists(file_name):
            file_name = name_parts[0] + (f" ({counter})" + name_parts[1])
            counter += 1
        return file_name

    def handle_receive_process(self):
        self._handle_receive_process()

    def receive_file(self, file_path=None):
        self.logger.info(f"{self.file_size} bytes will be received")
        file_name = self.get_valid_name(f"{file_path}")
        bytes_received = 0
        try:
            with open(file_name, "wb") as f:
                while bytes_received < self.file_size:
                    data = self.socket.receive_data()
                    f.write(data)
                    bytes_received += len(data)
                    self.logger.info(
                        f"Progress: {bytes_received/self.file_size * 100:.0f}%"
                    )
                return bytes_received
        except Exception as e:
            if bytes_received == self.file_size:
                self.logger.warning(
                    f"File {file_name} received successfully but something went wrong at the end"
                )
            else:
                self.logger.error(f"File {file_name} received with errors: {e}")
