from lib.protocol_handler import OperationCodes
from .file_handler import FileHandler


class FileUploader(FileHandler):
    def __init__(self, socket, client_address):
        super().__init__(socket, client_address)

    def run(self):
        op_code, seq_number, ack_number, data = self.socket.receive()
        if op_code != OperationCodes.CL_INFORMATION:
            raise Exception

        self.socket.send_ack()
        file_name, size = data.decode().split("#")
        with open(f"{file_name}", "wb") as f:
            while True:
                op_code, seq_number, ack_number, data = self.socket.receive()
                self.socket.send_ack()
                if op_code == OperationCodes.END:
                    break
                f.write(data)
            self.socket.socket.close()
