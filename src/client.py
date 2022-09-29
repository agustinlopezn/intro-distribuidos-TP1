import sys
from socket import *

from lib.custom_socket.saw_socket import SaWSocket
from lib.options import DownloadOptions, UploadOptions
from lib.process_handler.file_sender.client_file_sender import ClientFileSender
from lib.process_handler.file_receiver.client_file_receiver import ClientFileReceiver
from lib.protocol_handler import OperationCodes

HOST = "127.0.0.1"
CLIENT_PORT = 5000
BUFF_SIZE = 1024


class Client:
    @classmethod
    def upload():
        options = UploadOptions(sys.argv[1:])
        server_address = (options.host, options.port)
        ClientFileSender(
            options.file_name, server_address, HOST, CLIENT_PORT
        ).handle_send_process()

    @classmethod
    def download():
        options = DownloadOptions(sys.argv[1:])
        server_address = (options.host, options.port)
        ClientFileReceiver(
            options.file_name, server_address, HOST, CLIENT_PORT
        ).handle_receive_process()

