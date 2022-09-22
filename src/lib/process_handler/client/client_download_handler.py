from lib.custom_socket.saw_socket import SaWSocket
from lib.file_handler.file_receiver import FileReceiver
from lib.process_handler.client.client_handler import ClientHandler
from lib.protocol_handler import OperationCodes

PORT = 5000
BUFF_SIZE = 1024
FILE_NAME = "test.pdf"
DEST_FOLDER = "../files/downloaded/"


class ClientDownloadHandler(ClientHandler):
    def __init__(self, destination_address):
        socket = SaWSocket(destination_address=destination_address, timeout=3)
        self.file_receiver = FileReceiver(socket, destination_address, DEST_FOLDER)
        super().__init__(socket, destination_address)

    def handle_download(self, file_name):
        self.handle_process_start(file_name)
        bytes_received = self.file_receiver.receive_file(file_name)
        self.socket.close_connection(bytes_received, self.file_size)

    def handle_process_start(self, file_name):
        port = PORT
        data = self.socket.send_dl_request()
        port = int(data.decode())
        self.socket.destination_address = ("localhost", port)
        data = self.socket.send_file_information(file_name=file_name)
        self.file_size = int(data.decode())
        # Check size limits before sending ACK
        self.socket.send_ack()

    def close_connection(self, bytes_received):
        try:
            self.socket.send_end()
        except Exception as e:
            if bytes_received == self.file_size:
                print("File sent successfully")
            else:
                print(e)
        finally:
            print("Bytes received: ", bytes_received)
            self.socket.socket.close()

