import socket
from lib.protocol_handler import OperationCodes


class Accepter:
    def __init__(self, host, port, packet_type, socket_type):
        self.host = host
        self.port = port
        self.packet_type = packet_type
        self.socket_type = socket_type
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind((self.host, self.port))

    def listen(self, buff_size):
        msg, client_address = self.socket.recvfrom(buff_size)
        op_code = self.packet_type.get_op_code(msg.decode())
        if op_code not in (OperationCodes.DOWNLOAD, OperationCodes.UPLOAD):
            raise Exception("Invalid operation code")
        client = self.socket_type(client_address, self.packet_type)
        self.socket.sendto(
            self.packet_type.create_server_information(client.port), client_address
        )
        return op_code, client, client_address
