import sys
from socket import *

from lib.custom_socket.saw_socket import SaWSocket
from lib.process_handler.file_sender.client_file_sender import ClientFileSender
from lib.process_handler.file_receiver.client_file_receiver import ClientFileReceiver
from lib.protocol_handler import OperationCodes

PORT = 5000
BUFF_SIZE = 1024


def download(file_name):
    ClientFileReceiver(file_name, ("localhost", PORT)).handle_receive_process()


def upload(file_name):
    ClientFileSender(file_name, ("localhost", PORT)).handle_send_process()


if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("Usage: python3 client.py [download|upload]")
        exit(1)
    file_name = sys.argv[2] if len(sys.argv) == 3 else "test.pdf"
    if sys.argv[1] == "download":
        download(file_name)
    elif sys.argv[1] == "upload":
        upload(file_name)
    else:
        print("Usage: python3 client.py [download|upload] [file_name]")
        exit(1)
