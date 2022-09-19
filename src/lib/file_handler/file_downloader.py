from lib.protocol_handler import OperationCodes
from .file_handler import FileHandler


class FileDownloader(FileHandler):
    def __init__(self, socket, client_address):
        super().__init__(socket, client_address)

    def run(self):
        op_code, seq_number, ack_number, data = self.socket.receive()
        with open(f"../files/{data.decode()}", "rb") as file:
            while True:
                data = file.read(512)
                try:
                    self.socket.send_data(data)
                except Exception as e:
                    print(e)
                    break
                if not data:
                    break
            self.socket.socket.close()
            print("Data sent successfully")
