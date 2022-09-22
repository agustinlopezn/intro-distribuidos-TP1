from lib.protocol_handler import OperationCodes
from .file_handler import FileHandler

class FileReceiver(FileHandler):
    def __init__(self, socket, client_address, destination_folder):
        self.destination_folder = destination_folder
        super().__init__(socket, client_address)

    def receive_file(self, file_name, file_size):
        with open(f"{self.destination_folder}/{file_name}", "wb") as f:
            bytes_received = 0
            while bytes_received < file_size:
                op_code, data = self.socket.receive()
                self.socket.send_ack() # add to socket receive function
                f.write(data)
                bytes_received += len(data)
            return bytes_received

