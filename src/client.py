import sys
from socket import *

from lib.custom_socket.saw_socket import SaWSocket

PORT = 5000
BUFF_SIZE = 1024

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
        # import random
        # if random.randint(0, 10) == 0:
        #    print("DROPPING!!!" + str(pack_recv))
        #    continue
        s.send_ack()
        pack_recv += 1
        if not data:
            break
        f.write(data)
    s.socket.close()
