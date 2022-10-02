from socket import *
from threading import Thread

from src.lib.accepter import Accepter
from src.lib.logger import Logger
from src.lib.options import ServerOptions
from src.lib.file_handler.file_sender.server_file_sender import ServerFileSender
from src.lib.file_handler.file_receiver.server_file_receiver import ServerFileReceiver
from src.lib.operation_codes import OperationCodes
from src.lib.thread_cleaner import ThreadCleaner
from sys import argv

MAX_FILE_SIZE = 1073741824  # 1GB, in bytes


class Server(Thread):
    def __init__(self, options):
        super().__init__()
        self.threads = {}
        self.options = options

    def run(self):
        self.start_server()

    def stop(self):
        self.accepter.socket.close_connection()
        self.thread_cleaner.clean_threads()
        self.logger.info("Threads joined successfully")

    def start_server(self):
        if not self.options.valid():
            print("Error: some options are invalid")
            self.options.show_help = True
        if self.options.show_help:
            print("Usage: python3 start-server.py [-h] [-v] [-q] [-H host] [-p port]")
            exit(0)
        self.prepare_execution()
        while True:
            op_code, client_address, file_data = self.accepter.accept()
            if self.client_is_active(client_address):
                self.logger.error(f"Client {client_address} is already connected")
                continue
            if op_code == OperationCodes.DOWNLOAD:
                self.handle_download(file_data, client_address)
            elif op_code == OperationCodes.UPLOAD:
                self.handle_upload(file_data, client_address)

    def prepare_execution(self):
        self.logger = Logger("server", self.options.verbose, self.options.quiet)
        self.accepter = Accepter(
            host=self.options.host, port=self.options.port, logger=self.logger
        )
        self.thread_cleaner = ThreadCleaner(self.threads, self.logger)
        self.thread_cleaner.start()

    def handle_download(self, file_data, client_address):
        file_sender = ServerFileSender(
            file_data,
            source_dir=self.options.storage,
            opposite_address=client_address,
            logger=self.logger,
        )
        file_sender.handle_send_process()
        self.threads[client_address] = file_sender

    def handle_upload(self, file_data, client_address):
        file_receiver = ServerFileReceiver(
            file_data,
            dest_folder=self.options.storage,
            opposite_address=client_address,
            logger=self.logger,
        )
        file_receiver.handle_receive_process()
        self.threads[client_address] = file_receiver

    def client_is_active(self, client_address):
        # just in case that the cleaner hasn't run yet, checks that the thread is also alive
        return (
            client_address in self.threads and self.threads[client_address].is_alive()
        )


if __name__ == "__main__":
    Server().start_server()
