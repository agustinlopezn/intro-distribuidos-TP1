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

    def set_timeout(self, timeout):
        self.socket.settimeout(timeout)

    def send_data(self, message):
        raise NotImplementedError

    def receive(self):
        raise NotImplementedError

    def send_dl_request(self):
        raise NotImplementedError

    @property
    def port(self):
        return self.socket.getsockname()[1]
