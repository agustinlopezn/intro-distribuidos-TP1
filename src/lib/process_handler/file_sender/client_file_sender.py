from lib.custom_socket.saw_socket import SaWSocket
from lib.process_handler.file_sender.file_sender import FileSender
from lib.protocol_handler import OperationCodes

PORT = 5000
BUFF_SIZE = 1024
SRC_FOLDER = "../files/source"


class ClientFileSender(FileSender):
    def __init__(self, opposite_address):
        socket = SaWSocket(opposite_address=opposite_address, timeout=3)
        super().__init__(socket, opposite_address, SRC_FOLDER)

    def handle_send_process(self, file_name):
        self.handle_handshake(file_name)
        self.send_file(file_name, self.file_size, showProgress=True)
        self.socket.close_connection()

    def handle_handshake(self, file_name):
        port = PORT
        self.file_size = self.get_file_size(file_name)
        self.socket.send_up_request(file_name=file_name, file_size=self.file_size)
        self.socket.receive_sv_information()
        self.socket.send_nsq_ack()
