import os
from threading import Thread
from src.lib.file_handler.file_sender.file_sender import FileSender
from src.lib.operation_codes import OperationCodes


class ServerFileSender(FileSender, Thread):
    def __init__(self, file_data, **kwargs):
        super().__init__(**kwargs)
        self.file_name = file_data
        Thread.__init__(self)

    def run(self):
        self.handle_process_start()
        self.send_file()
        self.socket.close_connection()

    def _handle_send_process(self):
        # just for polymorphism purposes
        self.start()

    def handle_process_start(self):
        self.file_size = self.get_file_size(self.file_name)
        self.socket.send_sv_information(self.file_size)
