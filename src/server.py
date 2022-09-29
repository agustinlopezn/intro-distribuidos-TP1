from socket import *

from src.lib.accepter import Accepter
from src.lib.logger import Logger
from src.lib.options import ServerOptions
from src.lib.packet.gbn_packet import GBNPacket
from src.lib.packet.saw_packet import SaWPacket
from src.lib.process_handler.file_sender.server_file_sender import ServerFileSender
from src.lib.process_handler.file_receiver.server_file_receiver import (
    ServerFileReceiver,
)
from src.lib.protocol_handler import OperationCodes
from src.lib.custom_socket.gbn_socket import GBNSocket
from src.lib.custom_socket.saw_socket import SaWSocket
from src.lib.thread_cleaner import ThreadCleaner
from threading import Timer
from sys import argv

class Server:
    def __init__(self):
        self.threads = {}

    def start_server(self):
        options = ServerOptions(argv[1:])
        if options.show_help:
            print("Usage: python3 start-server.py [-h] [-v] [-q] [-H host] [-p port]")
            return
        logger = Logger("server", options.verbose, options.quiet)
        accepter = Accepter(host=options.host, port=options.port, logger=logger)
        thread_cleaner = ThreadCleaner(self.threads)
        thread_cleaner.start()
        while True:
            op_code, client_address, file_data = accepter.accept()
            if self.client_is_active(client_address):
                print(f"Client {client_address} is already connected")
                continue
            if op_code == OperationCodes.DOWNLOAD:
                file_sender = ServerFileSender(
                    file_data, opposite_address=client_address, logger=logger
                )
                file_sender.handle_send_process()
                self.threads[client_address] = file_sender
            elif op_code == OperationCodes.UPLOAD:
                file_receiver = ServerFileReceiver(
                    file_data, opposite_address=client_address, logger=logger
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
