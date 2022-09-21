from lib.protocol_handler import OperationCodes
from .file_handler import FileHandler
import os


class FileSender(FileHandler):
    def __init__(self, socket, client_address):
        super().__init__(socket, client_address)

    def send_file(self, file_name):
        with open(f"../files/{file_name}", "rb") as file:
            while True:
                data = file.read(512)
                try:
                    self.socket.send_data(data)
                except Exception as e:
                    print(e)
                    break
                if not data:
                    break
            self.socket.send_end()
            self.socket.socket.close()
            print("Data sent successfully")

    def get_file_size(self, file_name):
        return os.stat(f"../files/{file_name}").st_size


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

