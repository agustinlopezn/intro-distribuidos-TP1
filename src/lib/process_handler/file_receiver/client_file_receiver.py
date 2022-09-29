from threading import Thread
from src.lib.custom_socket.saw_socket import SaWSocket
from src.lib.process_handler.file_receiver.file_receiver import FileReceiver
from src.lib.protocol_handler import OperationCodes

PORT = 5000
BUFF_SIZE = 1024
DEST_FOLDER = "files/downloaded/"


class ClientFileReceiver(FileReceiver):
    def __init__(self, file_name, **kwargs):
        super().__init__(**kwargs)
        self.file_name = file_name

    def handle_receive_process(self):
        self.logger.info(f"Starting file receiving process for file {self.file_name}")
        self.handle_process_start()
        self.receive_file()
        self.socket.close_connection()

    def handle_process_start(self):
        port = PORT
        self.socket.send_dl_request(self.file_name)
        data = self.socket.receive_sv_information()
        port, file_size = data.decode().split("#")
        port, self.file_size = int(port), int(file_size)
        self.logger.info(f"{self.file_size} bytes will be received from port {port}")
        # Check size limits before sending ACK
        self.socket.send_nsq_ack()

