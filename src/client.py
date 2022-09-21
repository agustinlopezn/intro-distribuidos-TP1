import sys
from socket import *

from lib.custom_socket.saw_socket import SaWSocket
from lib.protocol_handler import OperationCodes
from lib.file_handler.file_receiver import recv_file_client
from lib.file_handler.file_sender import send_file_client

PORT = 5000
BUFF_SIZE = 1024


def download_client():
    file_name = "test.pdf"
    port = PORT
    s = SaWSocket(("localhost", port), timeout=3)
    s.send_dl_request()
    op_code, seq_number, ack_number, data = s.receive()
    port = int(data.decode())
    s.opposite_address = ("localhost", port)
    s.send_file_information(file_name=file_name)
    recv_file_client(s, file_name)


def upload_client():
    port = PORT
    s = SaWSocket(("localhost", port), timeout=1)
    s.send_up_request()
    op_code, seq_number, ack_number, data = s.receive()
    port = int(data.decode())
    s.opposite_address = ("localhost", port)
    send_file_client("test.pdf", s)


upload_client()
download_client()
