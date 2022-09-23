from lib.custom_socket.saw_socket import SaWSocket
from lib.file_handler.file_sender import FileSender
from lib.process_handler.client.client_handler import ClientHandler
from lib.protocol_handler import OperationCodes

PORT = 5000
BUFF_SIZE = 1024
SRC_FOLDER = "../files/source"


class ClientUploadHandler(ClientHandler):
    def __init__(self, destination_address):
        socket = SaWSocket(destination_address=("localhost", PORT), timeout=3)
        self.file_sender = FileSender(socket, destination_address, SRC_FOLDER)
        super().__init__(socket, destination_address)

    def handle_upload(self, file_name):
        self.handle_process_start(file_name)
        self.file_sender.send_file(file_name, self.file_size)
        self.socket.close_connection()

    def handle_process_start(self, file_name):
        port = PORT
        self.file_size = self.file_sender.get_file_size(file_name)
        self.socket.send_up_request(file_name=file_name, file_size=self.file_size)

        data = self.socket.receive_sv_information()
        
        port = int(data.decode())
        self.socket.destination_address = ("localhost", port)
        self.socket.send_nsq_ack()