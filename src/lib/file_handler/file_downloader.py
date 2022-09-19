from .file_handler import FileHandler


class FileDownloader(FileHandler):
    def __init__(self, socket, client_address):
        super().__init__(socket, client_address)

    def run(self):
        self.socket.send("hola".encode())
