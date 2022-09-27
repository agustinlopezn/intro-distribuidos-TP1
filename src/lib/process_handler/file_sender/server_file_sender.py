import os
from threading import Thread
from lib.process_handler.file_sender.file_sender import FileSender
from lib.protocol_handler import OperationCodes

SRC_FOLDER = "../files/uploaded/"


class ServerFileSender(FileSender, Thread):
    def __init__(self, socket, opposite_address, file_data):
        self.file_name = file_data
        super().__init__(socket, opposite_address, SRC_FOLDER)
        Thread.__init__(self)

    def run(self):
        self.handle_process_start()
        self.send_file(self.file_name, self.file_size)
        self.socket.close_connection()

    def handle_process_start(self):
        self.file_size = self.get_file_size(self.file_name)
        self.socket.send_sv_information(self.file_size)
