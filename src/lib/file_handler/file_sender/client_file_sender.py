import os
from time import time

from src.lib.file_handler.file_sender.file_sender import FileSender
from src.server import MAX_FILE_SIZE


class ClientFileSender(FileSender):
    def __init__(self, file_name, source_path, **kwargs):
        super().__init__(**kwargs)
        self.file_name = file_name
        self.source_path = source_path

    def is_valid_file(self):
        file_name = f"{self.source_path}"
        if not os.path.exists(file_name):
            self.logger.error(f"File {file_name} doesnt exist")
            return False
        file_size = os.stat(file_name).st_size
        if file_size > MAX_FILE_SIZE:
            self.logger.error(f"File {file_name} is too big")
            return False
        return True

    def _handle_send_process(self):
        if not self.is_valid_file():
            self.socket.close_connection()
            return
        start_time = time()
        self.logger.info(
            f"Starting file sending process for file {self.file_name} located in {self.source_path}"
        )
        # input(f"Client port is {self.socket.port}")
        self.handle_handshake()
        file_sent_success = self.send_file(f"{self.source_path}")
        self.socket.close_connection()
        finish_time = time()
        self.log_final_send_status(file_sent_success, finish_time - start_time)

    def handle_handshake(self):
        self.file_size = self.get_file_size(self.source_path)
        self.logger.info(
            f"{self.file_size} bytes will be sent to port {self.socket.port}"
        )
        self.socket.send_up_request(self.file_name, self.file_size)
