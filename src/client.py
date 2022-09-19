import sys
from socket import *

PORT = 5000
BUFF_SIZE = 1024

s = socket(AF_INET, SOCK_DGRAM)

port = PORT

s.sendto("0".encode(), ("localhost", port))
msg, address = s.recvfrom(BUFF_SIZE)
msg = msg.decode()
port = int(msg[1:])
s.sendto("3test.pdf".encode(), ("localhost", port))


import random

pack_recv = 0
with open("output", "wb") as f:
    while True:
        msg, address = s.recvfrom(BUFF_SIZE)

        # Randomly drop packets (10% chance)
        if random.randint(0, 10) == 0:
            print("DROPPING!!!" + str(pack_recv))
            continue

        s.sendto("5".encode(), ("localhost", port))
        pack_recv += 1
        if not msg:
            break
        f.write(msg)
    s.close()
