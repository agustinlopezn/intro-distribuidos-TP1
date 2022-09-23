import os
from lib.file_handler.file_sender import FileSender
from lib.process_handler.server.server_handler import ServerHandler
from lib.protocol_handler import OperationCodes

SRC_FOLDER = "../files/uploaded/"


class ServerDownloadHandler(ServerHandler):
    def __init__(self, socket, client_address, file_data):
        self.file_sender = FileSender(socket, client_address, SRC_FOLDER)
        self.file_name = file_data
        super().__init__(socket, client_address)

    def run(self):
        self.handle_process_start()
        self.file_sender.send_file(self.file_name, self.file_size)
        self.socket.close_connection()

    def handle_process_start(self):
        self.file_size = self.file_sender.get_file_size(self.file_name)
        self.socket.send_sv_information(self.file_size)

        file_size = self.file_sender.get_file_size(self.file_name)
        self.socket.send_file_information(file_size=file_size)
        self.file_size = file_size
