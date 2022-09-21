import os
from lib.file_handler.file_sender import FileSender
from lib.process_handler.server_handler import ServerHandler
from lib.protocol_handler import OperationCodes


class ServerDownloadHandler(ServerHandler):
    def __init__(self, socket, client_address):
        self.file_sender = FileSender(socket, client_address)
        super().__init__(socket, client_address)

    def run(self):
        self.handle_process_start()
        self.file_sender.send_file(self.file_name)

    def handle_process_start(self):
        op_code, seq_number, ack_number, data = self.socket.receive()
        if op_code != OperationCodes.FILE_INFORMATION:
            raise Exception

        self.file_name = data.decode()
        file_size = self.file_sender.get_file_size(self.file_name)
        self.socket.send_file_information(file_size=file_size)
