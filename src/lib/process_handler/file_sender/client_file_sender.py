from lib.custom_socket.saw_socket import SaWSocket
from lib.process_handler.file_sender.file_sender import FileSender
from lib.protocol_handler import OperationCodes

PORT = 5000
BUFF_SIZE = 1024
SRC_FOLDER = "../files/source"


class ClientFileSender(FileSender):
    def __init__(self, file_name, opposite_address):
        super().__init__(opposite_address, SRC_FOLDER)
        self.file_name = file_name

    def handle_send_process(self):
        self.handle_handshake()
        self.send_file()
        self.socket.close_connection()

    def handle_handshake(self):
        port = PORT
        self.file_size = self.get_file_size(self.file_name)
        self.socket.send_up_request(self.file_name, self.file_size)
        self.socket.receive_sv_information()
        self.socket.send_nsq_ack()
