import socket
from lib.custom_socket.saw_socket import SaWSocket
from lib.protocol_handler import OperationCodes


class Accepter:
    def __init__(self, host, port, Socket):
        self.Socket = Socket
        self.socket = Socket(opposite_address=None, host=host, port=port)
        self.socket.set_timeout(None)

    def accept(self):
        op_code, client_address, file_data = self.socket.receive_first_connection()
        
        new_socket = self.Socket(opposite_address=client_address, timeout=2)
        return op_code, new_socket, client_address, file_data
