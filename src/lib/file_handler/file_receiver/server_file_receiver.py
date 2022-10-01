from threading import Thread
from src.lib.file_handler.file_receiver.file_receiver import FileReceiver
from src.lib.file_handler.file_sender.file_sender import FileSender
from src.lib.operation_codes import OperationCodes
from socket import timeout


class ServerFileReceiver(FileReceiver, Thread):
    def run(self):
        pass

    def __init__(self, file_data, **kwargs):
        super().__init__(**kwargs)
        self.file_name = file_data.split("#")[0]
        self.file_size = int(file_data.split("#")[1])
        Thread.__init__(self)

    def run(self):
        self.logger.info(f"Starting file receiving process for file {self.file_name}")
        self.logger.info(
            f"{self.file_size} bytes will be received from port {self.socket.opposite_address[1]}"
        )
        try:
            self.handle_handshake()
            self.receive_file()
        except timeout:
            self.logger.error(
                f"Timeout reached while receiving, closing connection with client at port {self.socket.opposite_address[1]}"
            )
        finally:
            self.socket.close_connection(confirm_close=True)

    def _handle_receive_process(self):
        # just for polymorphism purposes
        self.start()

    def handle_handshake(self):
        self.socket.send_sv_information()
        # Check size limits before sending ACK

