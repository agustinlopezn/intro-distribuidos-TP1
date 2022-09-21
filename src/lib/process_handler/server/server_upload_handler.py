from lib.file_handler.file_receiver import FileReceiver
from lib.process_handler.server.server_handler import ServerHandler
from lib.protocol_handler import OperationCodes

DEST_FOLDER = "../files/uploaded/"


class ServerUploadHandler(ServerHandler):
    def run(self):
        pass

    def __init__(self, socket, client_address):
        self.file_receiver = FileReceiver(socket, client_address, DEST_FOLDER)
        super().__init__(socket, client_address)

    def run(self):
        self.handle_process_start()
        self.file_receiver.receive_file(self.file_name)

    def handle_process_start(self):
        op_code, seq_number, ack_number, data = self.socket.receive()
        if op_code != OperationCodes.FILE_INFORMATION:
            raise Exception

        file_name, size = data.decode().split("#")
        # Check size limits before sending ACK
        self.file_name = file_name
        self.socket.send_ack()

