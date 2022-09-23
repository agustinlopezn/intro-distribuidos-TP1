import sys
from socket import *

from lib.custom_socket.saw_socket import SaWSocket
from lib.process_handler.client.client_download_handler import ClientDownloadHandler
from lib.process_handler.client.client_upload_handler import ClientUploadHandler
from lib.protocol_handler import OperationCodes

PORT = 5000
BUFF_SIZE = 1024

def download(file_name):
    ClientDownloadHandler(("localhost", PORT)).handle_download(file_name)


def upload(file_name):
    ClientUploadHandler(("localhost", PORT)).handle_upload(file_name)

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
