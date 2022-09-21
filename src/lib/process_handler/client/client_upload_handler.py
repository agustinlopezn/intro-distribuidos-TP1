from lib.custom_socket.saw_socket import SaWSocket
from lib.file_handler.file_sender import FileSender
from lib.process_handler.client.client_handler import ClientHandler

PORT = 5000
BUFF_SIZE = 1024
SRC_FOLDER = "../files/source"


class ClientUploadHandler(ClientHandler):
    def __init__(self, opposite_address):
        socket = SaWSocket(("localhost", PORT), timeout=3)
        self.file_sender = FileSender(socket, opposite_address, SRC_FOLDER)
        super().__init__(socket, opposite_address)

    def handle_upload(self, file_name):
        self.handle_process_start(file_name)
        self.file_sender.send_file(file_name)

    def handle_process_start(self, file_name):
        port = PORT
        self.socket.send_up_request()
        op_code, seq_number, ack_number, data = self.socket.receive()
        port = int(data.decode())
        self.socket.opposite_address = ("localhost", port)

        file_size = self.file_sender.get_file_size(file_name)
        self.socket.send_file_information(file_name=file_name, file_size=file_size)
