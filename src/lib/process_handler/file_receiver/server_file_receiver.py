from threading import Thread
from lib.process_handler.file_receiver.file_receiver import FileReceiver
from lib.process_handler.file_sender.file_sender import FileSender
from lib.protocol_handler import OperationCodes

DEST_FOLDER = "../files/uploaded/"


class ServerFileReceiver(FileReceiver, Thread):
    def run(self):
        pass

    def __init__(self, opposite_address, file_data):
        super().__init__(opposite_address, DEST_FOLDER)
        self.file_name = file_data.split("#")[0]
        self.file_size = int(file_data.split("#")[1])
        Thread.__init__(self)

    def run(self):
        self.handle_handshake()
        self.receive_file()
        self.socket.close_connection()

    def handle_receive_process(self):
        # just for polymorphism purposes
        self.start()

    def handle_handshake(self):
        self.socket.send_sv_information()
        # Check size limits before sending ACK

