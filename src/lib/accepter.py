from src.lib.custom_socket.gbn_socket import GBNSocket
from src.lib.custom_socket.saw_socket import SaWSocket


class Accepter:
    def __init__(self, **kwargs):
        self.socket = GBNSocket(opposite_address=None, **kwargs)
        self.socket.set_timeout(None)

    def accept(self):
        op_code, client_address, file_data = self.socket.receive_first_connection()
        return op_code, client_address, file_data
