from socket import socket, AF_INET, SOCK_DGRAM, timeout
from src.lib.operation_codes import OperationCodes
from src.lib.saboteur import Saboteur
from src.lib.logger import Logger


class CustomSocket:
    __abstract__ = True

    def __init__(self, opposite_address=None, host="", port=0, logger=None):
        self.opposite_address = opposite_address
        self.socket = socket(AF_INET, SOCK_DGRAM)
        self.socket.bind((host, port))
        # Bind to a random port if no port and host are specified
        self.set_timeout(self.TIMEOUT)
        self.logger = logger
        self.saboteur = Saboteur(self._send, self.packet_type, logger)

    def _send(self, packet):
        seq_number = self.packet_type.determine_seq_number(packet[1:5])
        self.logger.debug(
            f"Sending packet with op_code {OperationCodes.op_name(packet[0])} and seq_number {seq_number} from port {self.port}"
        )
        if self.saboteur.sabotage_packet(packet):
            return
        try:
            self.socket.sendto(packet, self.opposite_address)
        except PermissionError as e:
            self.logger.warning(
                f"Dropping packet with op_code {OperationCodes.op_name(packet[0])} and seq_number {seq_number}"
            )

    #############################
    #   HANDSHAKE METHODS     #
    #############################

    def receive_sv_information(self):
        self.socket.settimeout(None)
        while True:
            data, address = self.socket.recvfrom(self.packet_type.MAX_PACKET_SIZE)
            op_code, seq_number, data = self.packet_type.parse_packet(data)
            if op_code == OperationCodes.SV_INTRODUCTION:
                self.logger.debug(f"Received server information: {data}")
                self.opposite_address = address
                self.socket.settimeout(self.TIMEOUT)
                return data

    def receive_first_connection(self):
        msg, client_address = self.socket.recvfrom(self.packet_type.MAX_PACKET_SIZE)
        op_code = self.packet_type.get_op_code(msg)
        self.logger.debug(
            f"Receiving first connection from client at port: {client_address[1]}"
        )
        if op_code not in (OperationCodes.DOWNLOAD, OperationCodes.UPLOAD):
            raise Exception("Invalid operation code")
        return op_code, client_address, self.packet_type.get_packet_data(msg).decode()

    def send_dl_request(self, file_name):
        self.logger.debug(
            f"Sending download request with port {self.port}, file_name {file_name}"
        )
        packet = self.generate_packet(
            op_code=OperationCodes.DOWNLOAD, data=file_name.encode()
        )
        return self._send(packet)

    def send_up_request(self, file_name, file_size=None):
        self.logger.debug(
            f"Sending upload request with port {self.port}, file_name {file_name} and file_size {file_size}"
        )
        data = self.serialize_information(file_name, file_size)
        packet = self.generate_packet(op_code=OperationCodes.UPLOAD, data=data)
        self._send(packet)

    #############################

    def set_timeout(self, timeout):
        self.socket.settimeout(timeout)

    def send_data(self, message):
        raise NotImplementedError

    def receive(self):
        raise NotImplementedError

    @property
    def port(self):
        return self.socket.getsockname()[1]
