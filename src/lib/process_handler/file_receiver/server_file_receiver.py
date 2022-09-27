from threading import Thread
from lib.process_handler.file_receiver.file_receiver import FileReceiver
from lib.process_handler.file_sender.file_sender import FileSender
from lib.protocol_handler import OperationCodes

DEST_FOLDER = "../files/uploaded/"


class ServerFileReceiver(FileReceiver, Thread):
    def run(self):
        pass

    def __init__(self, socket, client_address, file_data):
        self.file_name = file_data.split("#")[0]
        self.file_size = int(file_data.split("#")[1])
        super().__init__(socket, client_address, DEST_FOLDER)
        Thread.__init__(self)

    def run(self):
        self.handle_handshake()
        self.receive_file(
            self.file_name, self.file_size, showProgress=False
        )
        self.socket.close_connection()

    def handle_handshake(self):
        self.socket.send_sv_information()
        # Check size limits before sending ACK

