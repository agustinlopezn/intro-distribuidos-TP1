import sys
from socket import *

from lib.custom_socket.saw_socket import SaWSocket
from lib.protocol_handler import OperationCodes
from lib.file_handler.file_receiver import recv_file
from lib.file_handler.file_sender import send_file

PORT = 5000
BUFF_SIZE = 1024


def download_client():
    port = PORT
    s = SaWSocket(("localhost", port), timeout=3)
    s.send_dl_request()
    op_code, seq_number, ack_number, data = s.receive()
    port = int(data.decode())
    s.client_address = ("localhost", port)
    s.send_cl_information("test.pdf")
    recv_file("output.pdf", s)


def upload_client():
    port = PORT
    s = SaWSocket(("localhost", port), timeout=1)
    s.send_up_request()
    op_code, seq_number, ack_number, data = s.receive()
    port = int(data.decode())
    s.client_address = ("localhost", port)
    s.send_cl_information("test.pdf#1024")

    op_code, seq_number, ack_number, data = s.receive()
    if op_code != OperationCodes.ACK:
        return
    send_file("test.pdf", s)


upload_client()
download_client()
