from time import time

from lib.file_handler.file_receiver.file_receiver import FileReceiver


class ClientFileReceiver(FileReceiver):
    def __init__(self, file_name, dest_path, **kwargs):
        super().__init__(**kwargs)
        self.file_name = file_name
        self.destination_path = dest_path

    def _handle_receive_process(self):
        start_time = time()
        self.logger.info(
            f"Starting file receiving process for file {self.file_name} to be stored in {self.destination_path}"
        )
        input(f"Client port is {self.socket.port}. Press enter to start request...")
        self.handle_process_start()
        if self.file_size == -1:
            self.logger.error(f"File {self.file_name} not found on server")
            self.socket.close_connection()
            return

        file_recvd_success = self.receive_file()
        self.socket.close_connection(confirm_close=file_recvd_success)
        finish_time = time()
        self.log_final_receive_status(file_recvd_success, finish_time - start_time)

    def handle_process_start(self):
        data = self.socket.send_dl_request(self.file_name)
        # Check size limits before sending ACK
        port, self.file_size, file_name = self.socket.deserialize_information(
            data.decode()
        )
