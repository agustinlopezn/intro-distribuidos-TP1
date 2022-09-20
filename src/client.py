import sys
from socket import *

from lib.custom_socket.saw_socket import SaWSocket
from lib.protocol_handler import OperationCodes

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

    pack_recv = 0
    with open("output", "wb") as f:
        while True:
            op_code, seq_number, ack_number, data = s.receive()
            # Randomly drop packets (10% chance)
            import random
            if random.randint(0, 10) == 0:
                print("DROPPING!!!" + str(pack_recv))
                continue
            s.send_ack()
            pack_recv += 1
            if not data:
                break
            f.write(data)
        s.socket.close()

def upload_client():
    port = PORT
    s = SaWSocket(("localhost", port), timeout=3)
    s.send_up_request()
    op_code, seq_number, ack_number, data = s.receive()
    port = int(data.decode())
    s.client_address = ("localhost", port)
    s.send_cl_information("test.pdf#1024")

    op_code, seq_number, ack_number, data = s.receive()
    if op_code != OperationCodes.ACK:
        return
    
    with open(f"../files/test.pdf", "rb") as file:
        while True:
            data = file.read(512)
            try:
                s.send_data(data)
            except Exception as e:
                print(e)
                break
            if not data:
                break
        s.send_end()
        s.socket.close()
        print("Data sent successfully")

upload_client()