from lib.protocol_handler import OperationCodes
from .file_handler import FileHandler


class FileReceiver(FileHandler):
    def __init__(self, socket, client_address):
        super().__init__(socket, client_address)

    def recv_file(self, file_name):
        recv_file(self.socket, file_name=file_name)


def recv_file(socket, file_name):
    with open(f"{file_name}", "wb") as f:
        while True:
            op_code, seq_number, ack_number, data = socket.receive()
            socket.send_ack()
            if op_code == OperationCodes.END:
                break
            f.write(data)
        socket.socket.close()

def recv_file_client(socket, file_name):
    op_code, seq_number, ack_number, data = socket.receive()
    if op_code != OperationCodes.FILE_INFORMATION:
        raise Exception

    file_size = int(data.decode())
    # Check size limits before sending ACK
    socket.send_ack()
    with open(f"{file_name}", "wb") as f:
        while True:
            op_code, seq_number, ack_number, data = socket.receive()
            socket.send_ack()
            if op_code == OperationCodes.END:
                break
            f.write(data)
        socket.socket.close()
