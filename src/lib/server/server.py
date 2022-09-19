from socket import *


PORT = 5000
BUFF_SIZE = 1024



s = socket(AF_INET, SOCK_DGRAM)

 

# Bind to address and ip

s.bind(("localhost", PORT))

 

print("Server up and running!")

while(True):
    msg, address = s.recvfrom(BUFF_SIZE)
    print("Received: ", msg.decode())
    response = "Message received: " + msg.decode()
    s.sendto(response.encode(), address)