from threading import Thread
from src.lib.custom_socket.saw_socket import SaWSocket
from src.lib.file_handler.file_receiver.file_receiver import FileReceiver
from src.lib.operation_codes import OperationCodes
from time import time


class ClientFileReceiver(FileReceiver):
    def __init__(self, file_name, dest_path, **kwargs):
        super().__init__(**kwargs)
        self.file_name = file_name
        self.dest_path = dest_path

    def _handle_receive_process(self):
        start_time = time()
        self.logger.info(
            f"Starting file receiving process for file {self.file_name} to be stored in {self.dest_path}"
        )
        self.handle_process_start()
        if self.file_size == -1:
            self.logger.error(f"File {self.file_name} not found on server")
            self.socket.close_connection(confirm_close=False)
            return
        self.receive_file(f"{self.dest_path}")
        self.socket.close_connection(confirm_close=True)
        finish_time = time()
        self.logger.info(
            f"File {self.file_name} received in %.2f seconds"
            % (finish_time - start_time)
        )

    def handle_process_start(self):
        data = self.socket.send_dl_request(self.file_name)
        # Check size limits before sending ACK
        port, file_size = data.decode().split("#")
        port, self.file_size = int(port), int(file_size)
