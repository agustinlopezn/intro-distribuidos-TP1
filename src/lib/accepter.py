from src.lib.custom_socket.gbn_socket import GBNSocket
from src.lib.custom_socket.saw_socket import SaWSocket
from dotenv import load_dotenv
import os

load_dotenv()


class Accepter:
    def __init__(self, **kwargs):
        socket_type = SaWSocket if os.getenv("SOCKET_TYPE") == "SaW" else GBNSocket
        self.socket = socket_type(opposite_address=None, **kwargs)
        self.socket.set_timeout(None)

    def accept(self):
        op_code, client_address, file_data = self.socket.receive_first_connection()
        return op_code, client_address, file_data
