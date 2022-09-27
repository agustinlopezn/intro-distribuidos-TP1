import socket
from lib.custom_socket.saw_socket import SaWSocket
from lib.protocol_handler import OperationCodes


class Accepter:
    def __init__(self, host, port, socket_type):
        self.socket_type = socket_type
        self.socket = socket_type(opposite_address=None, host=host, port=port)
        self.socket.set_timeout(None)

    def accept(self):
        op_code, client_address, file_data = self.socket.receive_first_connection()
        
        new_socket = self.socket_type(opposite_address=client_address, timeout=3)
        return op_code, new_socket, client_address, file_data
