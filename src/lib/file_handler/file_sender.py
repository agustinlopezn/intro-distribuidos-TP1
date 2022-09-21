from lib.protocol_handler import OperationCodes
from .file_handler import FileHandler
import os


class FileSender(FileHandler):
    def __init__(self, socket, client_address):
        super().__init__(socket, client_address)

    def run(self):
        op_code, seq_number, ack_number, data = self.socket.receive()
        if op_code != OperationCodes.FILE_INFORMATION:
            raise Exception
        send_file(data.decode(), self.socket)


def send_file(file_name, socket):
    with open(f"../files/{file_name}", "rb") as file:
        file_stats = os.stat(file_name)
        socket.send_file_information(file_size=file_stats.st_size)
        # no need to send name back to client
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


def send_file_client(file_name, socket):
    with open(f"../files/{file_name}", "rb") as file:
        file_stats = os.stat(file_name)
        socket.send_file_information(file_name=file_name, file_size=file_stats.st_size)
        # no need to send name back to client
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
