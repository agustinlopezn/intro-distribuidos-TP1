import sys
from socket import *

PORT = 5000
BUFF_SIZE = 1024

s = socket(AF_INET, SOCK_DGRAM)

port = PORT
for line in sys.stdin:
    s.sendto(line.encode(), ('localhost', port))
    msg, address = s.recvfrom(BUFF_SIZE)
    print(msg.decode())
    msg = msg.decode()
    if msg[0] == '2':
        port = int(msg[1:])
