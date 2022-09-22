from lib.protocol_handler import OperationCodes
from .file_handler import FileHandler

class FileReceiver(FileHandler):
    def __init__(self, socket, client_address, destination_folder):
        self.destination_folder = destination_folder
        super().__init__(socket, client_address)

    def receive_file(self, file_name):
        with open(f"{self.destination_folder}/{file_name}", "wb") as f:
            bytes_received = 0
            while True:
                op_code, data = self.socket.receive()
                self.socket.send_ack()
                if op_code == OperationCodes.END:
                    print("Ending connection")
                    break
                f.write(data)
                bytes_received += len(data)
            return bytes_received

