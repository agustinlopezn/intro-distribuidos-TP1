from threading import Thread
from lib.custom_socket.saw_socket import SaWSocket
from lib.process_handler.file_receiver.file_receiver import FileReceiver
from lib.protocol_handler import OperationCodes

PORT = 5000
BUFF_SIZE = 1024
DEST_FOLDER = "../files/downloaded/"


class ClientFileReceiver(FileReceiver):
    def __init__(self, file_name, opposite_address):
        super().__init__(opposite_address, DEST_FOLDER)
        self.file_name = file_name

    def handle_receive_process(self):
        self.handle_process_start()
        self.receive_file()
        self.socket.close_connection()

    def handle_process_start(self):
        port = PORT
        self.socket.send_dl_request(self.file_name)
        data = self.socket.receive_sv_information()
        port, file_size = data.decode().split("#")
        port, self.file_size = int(port), int(file_size)
        # Check size limits before sending ACK
        self.socket.send_nsq_ack()

