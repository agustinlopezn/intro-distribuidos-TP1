from lib.protocol_handler import OperationCodes
from .file_handler import FileHandler


class FileSender(FileHandler):
    def __init__(self, socket, client_address):
        super().__init__(socket, client_address)

    def run(self):
        op_code, seq_number, ack_number, data = self.socket.receive()
        if op_code != OperationCodes.CL_INFORMATION:
            raise Exception
        send_file(data.decode(), self.socket)


def send_file(file_name, socket):
    with open(f"../files/{file_name}", "rb") as file:
        while True:
            data = file.read(512)
            try:
                socket.send_data(data)
            except Exception as e:
                print(e)
                break
            if not data:
                break
        socket.send_end()
        socket.socket.close()
        print("Data sent successfully")
