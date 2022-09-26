from socket import *

from lib.accepter import Accepter
from lib.file_handler.file_sender import FileSender
from lib.file_handler.file_receiver import FileReceiver
from lib.packet.gbn_packet import GBNPacket
from lib.packet.saw_packet import SaWPacket
from lib.process_handler.server.server_download_handler import ServerDownloadHandler
from lib.process_handler.server.server_upload_handler import ServerUploadHandler
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
    Socket = SaWSocket
else:
    Socket = GBNSocket
THREADS = {}


def start_server():
    accepter = Accepter(HOST, PORT, Socket)
    thread_cleaner = ThreadCleaner(THREADS)
    thread_cleaner.start()
    while True:
        op_code, client_socket, client_address, file_data = accepter.accept()
        if client_is_active(client_address):
            print(f"Client {client_address} is already connected")
            continue
        if op_code == OperationCodes.DOWNLOAD:
            thread = ServerDownloadHandler(client_socket, client_address, file_data)
        elif op_code == OperationCodes.UPLOAD:
            thread = ServerUploadHandler(client_socket, client_address, file_data)
        thread.start()
        THREADS[client_address] = thread

def client_is_active(client_address):
    # just in case that the cleaner hasn't run yet, checks that the thread is also alive
    return client_address in THREADS and THREADS[client_address].is_alive()

if __name__ == "__main__":
    start_server()