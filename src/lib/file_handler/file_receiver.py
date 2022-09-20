from lib.protocol_handler import OperationCodes
from .file_handler import FileHandler


class FileReceiver(FileHandler):
    def __init__(self, socket, client_address):
        super().__init__(socket, client_address)

    def run(self):
        op_code, seq_number, ack_number, data = self.socket.receive()
        if op_code != OperationCodes.CL_INFORMATION:
            raise Exception
        file_name, size = data.decode().split("#")
        # Check size limits before sending ACK
        self.socket.send_ack()
        recv_file(file_name, self.socket)


def recv_file(file_name, socket):
    with open(f"{file_name}", "wb") as f:
        while True:
            op_code, seq_number, ack_number, data = socket.receive()
            socket.send_ack()
            if op_code == OperationCodes.END:
                break
            f.write(data)
        socket.socket.close()
