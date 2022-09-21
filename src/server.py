from socket import *

from lib.accepter import Accepter
from lib.file_handler.file_sender import FileSender
from lib.file_handler.file_receiver import FileReceiver
from lib.packet.gbn_packet import GBNPacket
from lib.packet.saw_packet import SaWPacket
from lib.process_handler.server_download_handler import ServerDownloadHandler
from lib.process_handler.server_upload_handler import ServerUploadHandler
from lib.protocol_handler import OperationCodes
from lib.custom_socket.gbn_socket import GBNSocket
from lib.custom_socket.saw_socket import SaWSocket

HOST = "localhost"
PORT = 5000
BUFF_SIZE = 1024
PROTOCOL_TYPE = "SaW"
if PROTOCOL_TYPE == "SaW":
    packet_type = SaWPacket
    socket_type = SaWSocket
else:
    packet_type = GBNPacket
    socket_type = GBNSocket


accepter = Accepter(HOST, PORT, packet_type, socket_type)

while True:
    op_code, client, address = accepter.listen(BUFF_SIZE)
    if op_code == OperationCodes.DOWNLOAD:
        ServerDownloadHandler(client, address).start()
    else:
        ServerUploadHandler(client, address).start()
