from lib.custom_socket.saw_socket import SaWSocket
from lib.file_handler.file_receiver import FileReceiver
from lib.process_handler.client.client_handler import ClientHandler
from lib.protocol_handler import OperationCodes

PORT = 5000
BUFF_SIZE = 1024
FILE_NAME = "test.pdf"
DEST_FOLDER = "../files/downloaded/"


class ClientDownloadHandler(ClientHandler):
    def __init__(self, opposite_address):
        socket = SaWSocket(("localhost", PORT), timeout=3)
        self.file_receiver = FileReceiver(socket, opposite_address, DEST_FOLDER)
        super().__init__(socket, opposite_address)

    def handle_download(self, file_name):
        self.handle_process_start(file_name)
        self.file_receiver.receive_file(file_name)

    def handle_process_start(self, file_name):
        port = PORT
        self.socket.send_dl_request()
        op_code, seq_number, ack_number, data = self.socket.receive()
        port = int(data.decode())
        self.socket.opposite_address = ("localhost", port)
        self.socket.send_file_information(file_name=file_name)
        op_code, seq_number, ack_number, data = self.socket.receive()

        if op_code != OperationCodes.FILE_INFORMATION:
            raise Exception

        file_size = int(data.decode())
        # Check size limits before sending ACK
        self.socket.send_ack()
