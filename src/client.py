import sys
from socket import *

PORT = 5000
BUFF_SIZE = 1024

s = socket(AF_INET, SOCK_DGRAM)


for line in sys.stdin:
    s.sendto(line.encode(), ('localhost', PORT))
    msg, address = s.recvfrom(BUFF_SIZE)
    print(msg.decode())