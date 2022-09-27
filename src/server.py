from socket import *

from lib.accepter import Accepter
from lib.packet.gbn_packet import GBNPacket
from lib.packet.saw_packet import SaWPacket
from lib.process_handler.file_sender.server_file_sender import ServerFileSender
from lib.process_handler.file_receiver.server_file_receiver import ServerFileReceiver
from lib.protocol_handler import OperationCodes
from lib.custom_socket.gbn_socket import GBNSocket
from lib.custom_socket.saw_socket import SaWSocket
from lib.thread_cleaner import ThreadCleaner
from threading import Timer

HOST = "localhost"
PORT = 5000
BUFF_SIZE = 1024
PROTOCOL = "SaW"
if PROTOCOL == "SaW":
    custom_socket = SaWSocket
else:
    custom_socket = GBNSocket
THREADS = {}


def start_server():
    accepter = Accepter(HOST, PORT, custom_socket)
    thread_cleaner = ThreadCleaner(THREADS)
    thread_cleaner.start()
    while True:
        op_code, client_address, file_data = accepter.accept()
        if client_is_active(client_address):
            print(f"Client {client_address} is already connected")
            continue
        if op_code == OperationCodes.DOWNLOAD:
            file_sender = ServerFileSender(client_address, file_data)
            file_sender.handle_send_process()
            THREADS[client_address] = file_sender
        elif op_code == OperationCodes.UPLOAD:
            file_receiver = ServerFileReceiver(client_address, file_data)
            file_receiver.handle_receive_process()
            THREADS[client_address] = file_receiver


def client_is_active(client_address):
    # just in case that the cleaner hasn't run yet, checks that the thread is also alive
    return client_address in THREADS and THREADS[client_address].is_alive()


if __name__ == "__main__":
    start_server()
