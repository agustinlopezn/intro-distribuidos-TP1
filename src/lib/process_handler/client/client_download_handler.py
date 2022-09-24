from lib.custom_socket.saw_socket import SaWSocket
from lib.file_handler.file_receiver import FileReceiver
from lib.process_handler.client.client_handler import ClientHandler
from lib.protocol_handler import OperationCodes

PORT = 5000
BUFF_SIZE = 1024
DEST_FOLDER = "../files/downloaded/"


class ClientDownloadHandler(ClientHandler):
    def __init__(self, destination_address):
        socket = SaWSocket(destination_address=destination_address, timeout=3)
        self.file_receiver = FileReceiver(socket, destination_address, DEST_FOLDER)
        super().__init__(socket, destination_address)

    def handle_download(self, file_name):
        self.handle_process_start(file_name)
        self.file_receiver.receive_file(file_name, self.file_size, showProgress=True)
        self.socket.close_connection()

    def handle_process_start(self, file_name):
        port = PORT
        self.socket.send_dl_request(file_name)
        data = self.socket.receive_sv_information()
            
        port, file_size = data.decode().split("#")
        port, self.file_size = int(port), int(file_size)
        self.socket.destination_address = ("localhost", port)
        # Check size limits before sending ACK
        self.socket.send_nsq_ack()

