import sys
from socket import *

from lib.custom_socket.saw_socket import SaWSocket
from lib.process_handler.client.client_download_handler import ClientDownloadHandler
from lib.process_handler.client.client_upload_handler import ClientUploadHandler
from lib.protocol_handler import OperationCodes

PORT = 5000
BUFF_SIZE = 1024


def download():
    ClientDownloadHandler(("localhost", PORT)).handle_download("test.pdf")


def upload():
    ClientUploadHandler(("localhost", PORT)).handle_upload("test.pdf")


upload()
download()
