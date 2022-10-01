from threading import Thread
from src.lib.custom_socket.saw_socket import SaWSocket
from src.lib.file_handler.file_receiver.file_receiver import FileReceiver
from src.lib.operation_codes import OperationCodes

DEST_FOLDER = "files/downloaded/"


class ClientFileReceiver(FileReceiver):
    def __init__(self, file_name, **kwargs):
        super().__init__(**kwargs)
        self.file_name = file_name

    def _handle_receive_process(self):
        self.logger.info(f"Starting file receiving process for file {self.file_name}")
        self.handle_process_start()
        self.receive_file()
        self.socket.close_connection(confirm_close=True)

    def handle_process_start(self):
        data = self.socket.send_dl_request(self.file_name)
        # Check size limits before sending ACK
        port, file_size = data.decode().split("#")
        port, self.file_size = int(port), int(file_size)
        self.logger.info(f"{self.file_size} bytes will be received from port {port}")
