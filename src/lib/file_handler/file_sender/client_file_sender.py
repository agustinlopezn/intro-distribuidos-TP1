from src.lib.custom_socket.saw_socket import SaWSocket
from src.lib.file_handler.file_sender.file_sender import FileSender
from src.lib.operation_codes import OperationCodes


class ClientFileSender(FileSender):
    def __init__(self, file_name, **kwargs):
        super().__init__(**kwargs)
        self.file_name = file_name

    def handle_send_process(self):
        self.logger.info(f"Starting file sending process for file {self.file_name}")
        self.handle_handshake()
        self.send_file()
        self.socket.close_connection()

    def handle_handshake(self):
        self.file_size = self.get_file_size(self.file_name)
        self.logger.info(
            f"{self.file_size} bytes will be sent to port {self.socket.port}"
        )
        self.socket.send_up_request(self.file_name, self.file_size)
        self.socket.receive_sv_information()
        self.socket.send_nsq_ack()
