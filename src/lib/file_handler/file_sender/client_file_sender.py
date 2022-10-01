from src.lib.custom_socket.saw_socket import SaWSocket
from src.lib.file_handler.file_sender.file_sender import FileSender
from src.lib.operation_codes import OperationCodes
from time import time

class ClientFileSender(FileSender):
    def __init__(self, file_name, **kwargs):
        super().__init__(**kwargs)
        self.file_name = file_name

    def _handle_send_process(self):
        start_time = time()
        self.logger.info(f"Starting file sending process for file {self.file_name}")
        input(f"Client port is {self.socket.port}")
        self.handle_handshake()
        self.send_file()
        self.socket.close_connection()
        finish_time = time()
        self.logger.info(
            f"File {self.file_name} sent in %.2f seconds" % (finish_time - start_time)
        )

    def handle_handshake(self):
        self.file_size = self.get_file_size(self.file_name)
        self.logger.info(
            f"{self.file_size} bytes will be sent to port {self.socket.port}"
        )
        self.socket.send_up_request(self.file_name, self.file_size)
