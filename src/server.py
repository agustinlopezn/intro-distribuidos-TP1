from socket import *

from lib.accepter import Accepter
from lib.logger import Logger
from lib.options import ServerOptions
from lib.packet.gbn_packet import GBNPacket
from lib.packet.saw_packet import SaWPacket
from lib.process_handler.file_sender.server_file_sender import ServerFileSender
from lib.process_handler.file_receiver.server_file_receiver import ServerFileReceiver
from lib.protocol_handler import OperationCodes
from lib.custom_socket.gbn_socket import GBNSocket
from lib.custom_socket.saw_socket import SaWSocket
from lib.thread_cleaner import ThreadCleaner
from threading import Timer
from sys import argv

HOST = "localhost"
SERVER_PORT = 5000
BUFF_SIZE = 1024
PROTOCOL = "SaW"
if PROTOCOL == "SaW":
    custom_socket = SaWSocket
else:
    custom_socket = GBNSocket
THREADS = {}


class Server:

    @classmethod
    def start_server(self):
        options = ServerOptions(argv[1:])
        if options.show_help:
            print("Usage: python3 start-server.py [-h] [-v] [-q] [-H host] [-p port]")
            return
        logger = Logger("server", options.verbose, options.quiet)
        accepter = Accepter(options.host, options.port, custom_socket)
        thread_cleaner = ThreadCleaner(THREADS)
        thread_cleaner.start()
        while True:
            op_code, client_address, file_data = accepter.accept()
            if self.client_is_active(client_address):
                print(f"Client {client_address} is already connected")
                continue
            if op_code == OperationCodes.DOWNLOAD:
                file_sender = ServerFileSender(
                    file_data, client_address=client_address, logger=logger
                )
                file_sender.handle_send_process()
                THREADS[client_address] = file_sender
            elif op_code == OperationCodes.UPLOAD:
                file_receiver = ServerFileReceiver(
                    file_data, client_address=client_address, logger=logger
                )
                file_receiver.handle_receive_process()
                THREADS[client_address] = file_receiver

    def client_is_active(self, client_address):
        # just in case that the cleaner hasn't run yet, checks that the thread is also alive
        return client_address in THREADS and THREADS[client_address].is_alive()


if __name__ == "__main__":
    Server().start_server()
