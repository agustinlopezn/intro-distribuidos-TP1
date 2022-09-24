from lib.file_handler.file_receiver import FileReceiver
from lib.process_handler.server.server_handler import ServerHandler
from lib.protocol_handler import OperationCodes

DEST_FOLDER = "../files/uploaded/"


class ServerUploadHandler(ServerHandler):
    def run(self):
        pass

    def __init__(self, socket, client_address, file_data):
        self.file_receiver = FileReceiver(socket, client_address, DEST_FOLDER)
        self.file_name = file_data.split("#")[0]
        self.file_size = int(file_data.split("#")[1])
        super().__init__(socket, client_address)

    def run(self):
        self.handle_process_start()
        self.file_receiver.receive_file(self.file_name, self.file_size, showProgress=False)
        self.socket.close_connection()

    def handle_process_start(self):
        self.socket.send_sv_information()
        # Check size limits before sending ACK

