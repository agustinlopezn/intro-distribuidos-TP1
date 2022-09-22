from socket import *

from lib.accepter import Accepter
from lib.file_handler.file_sender import FileSender
from lib.file_handler.file_receiver import FileReceiver
from lib.packet.gbn_packet import GBNPacket
from lib.packet.saw_packet import SaWPacket
from lib.process_handler.server.server_download_handler import ServerDownloadHandler
from lib.process_handler.server.server_upload_handler import ServerUploadHandler
from lib.protocol_handler import OperationCodes
from lib.custom_socket.gbn_socket import GBNSocket
from lib.custom_socket.saw_socket import SaWSocket

HOST = "localhost"
PORT = 5000
BUFF_SIZE = 1024
PROTOCOL = "SaW"
if PROTOCOL == "SaW":
    Socket = SaWSocket
else:
    Socket = GBNSocket


accepter = Accepter(HOST, PORT, Socket)

while True:
    op_code, client_socket, client_address = accepter.accept()
    if op_code == OperationCodes.DOWNLOAD:
        ServerDownloadHandler(client_socket, client_address).start()
    else:
        ServerUploadHandler(client_socket, client_address).start()
