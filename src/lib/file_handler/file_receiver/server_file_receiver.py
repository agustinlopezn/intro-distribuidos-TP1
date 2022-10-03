from threading import Thread
from time import time

from src.lib.file_handler.file_receiver.file_receiver import FileReceiver


class ServerFileReceiver(FileReceiver, Thread):
    def run(self):
        pass

    def __init__(self, file_data, dest_folder, **kwargs):
        super().__init__(**kwargs)
        port, file_size, file_name = self.socket.deserialize_information(file_data)
        self.file_size = file_size
        self.file_name = file_name
        self.destination_path = f"{dest_folder}/{self.file_name}"
        Thread.__init__(self)

    def run(self):
        start_time = time()
        self.logger.info(f"Starting file receiving process for file {self.file_name}")
        self.destination_path, self.file_name = self.get_valid_name(
            self.destination_path
        )
        self.handle_handshake()
        file_recvd_success = self.receive_file()
        self.socket.close_connection(confirm_close=True)
        finish_time = time()
        self.log_final_receive_status(file_recvd_success, finish_time - start_time)

    def _handle_receive_process(self):
        # just for polymorphism purposes
        self.start()

    def handle_handshake(self):
        self.socket.send_sv_information(file_name=self.file_name)
        # Check size limits before sending ACK
