import socket
from lib.custom_socket.saw_socket import SaWSocket
from lib.protocol_handler import OperationCodes


class Accepter:
    def __init__(self, host, port, packet_type, socket_type):
        self.host = host
        self.port = port
        self.packet_type = packet_type
        self.socket_type = socket_type
        self.socket = SaWSocket(opposite_address=None, host=host, port=port)

    def listen(self, buff_size):
        op_code, client_address = self.socket.receive_first_connection()
        self.socket.set_opposite_address(client_address)
        new_socket = self.socket_type(opposite_address=client_address, timeout=2)
        self.socket.send_sv_information(new_socket.port)
        return op_code, new_socket, client_address
