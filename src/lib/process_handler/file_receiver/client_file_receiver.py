from threading import Thread
from lib.custom_socket.saw_socket import SaWSocket
from lib.process_handler.file_receiver.file_receiver import FileReceiver
from lib.protocol_handler import OperationCodes

PORT = 5000
BUFF_SIZE = 1024
DEST_FOLDER = "../files/downloaded/"


class ClientFileReceiver(FileReceiver):
    def __init__(self, opposite_address):
        socket = SaWSocket(opposite_address=opposite_address, timeout=3)
        super().__init__(socket, opposite_address, DEST_FOLDER)

    def handle_receive_process(self, file_name):
        self.handle_process_start(file_name)
        self.receive_file(file_name, self.file_size, showProgress=True)
        self.socket.close_connection()

    def handle_process_start(self, file_name):
        port = PORT
        self.socket.send_dl_request(file_name)
        data = self.socket.receive_sv_information()
            
        port, file_size = data.decode().split("#")
        port, self.file_size = int(port), int(file_size)
        self.socket.opposite_address = ("localhost", port)
        # Check size limits before sending ACK
        self.socket.send_nsq_ack()

