from socket import AF_INET, SOCK_DGRAM, socket, timeout

from src.lib.operation_codes import OperationCodes
from src.lib.saboteur import Saboteur


class CustomSocket:
    __abstract__ = True

    def __init__(
        self,
        packet_type,
        seq_number,
        opposite_address=None,
        host="",
        port=0,
        logger=None,
    ):
        self.opposite_address = opposite_address
        self.socket = socket(AF_INET, SOCK_DGRAM)
        self.socket.bind((host, port))
        # Bind to a random port if no port and host are specified
        self.set_timeout(self.TIMEOUT)
        self.logger = logger
        self.packet_type = packet_type
        self.saboteur = Saboteur(self._send, self.packet_type, logger)
        self.seq_number = seq_number

    #############################
    #      SENDING METHODS      #
    #############################

    def send_nsq_ack(self):
        self.logger.debug("Sending NSQ_ACK")
        packet = self.generate_packet(op_code=OperationCodes.NSQ_ACK)
        self._send(packet)

    def _send(self, packet):
        seq_number = self.packet_type.get_seq_number(packet)
        self.logger.debug(
            f"Sending packet with op_code {OperationCodes.op_name(packet[0])} and seq_number {seq_number} from chunk {self.chunk_number}"
        )
        if self.saboteur.sabotage_packet(packet):
            return
        try:
            self.socket.sendto(packet, self.opposite_address)
        except PermissionError as e:
            self.logger.warning(
                f"Dropping packet with op_code {OperationCodes.op_name(packet[0])} and seq_number {seq_number} from chunk {self.chunk_number}"
            )

    def _send_and_wait(self, op_code, data, expected_op_code=None):
        packet = self.generate_packet(op_code, data)
        for i in range(self.MAX_ATTEMPS):
            try:
                self._send(packet)
                data = self.receive_response(expected_op_code=expected_op_code)
                return data
            except timeout:
                self.logger.warning("TIMEOUT! Retrying...")
        raise Exception("Connection timed out")

    #############################
    #     RECEIVING METHODS     #
    #############################

    def receive_ack(self):
        while True:
            data, address = self.socket.recvfrom(self.packet_type.MAX_PACKET_SIZE)
            op_code = self.packet_type.get_op_code(data)
            seq_number = self.packet_type.get_seq_number(data)
            if op_code == OperationCodes.ACK and self.valid_packet(address, seq_number):
                self.logger.debug(f"Received ack with seq_number {seq_number}")
                self.update_seq_number()
                return

    def receive_nsq_ack(self):
        while True:
            data, address = self.socket.recvfrom(self.packet_type.MAX_PACKET_SIZE)
            op_code = self.packet_type.get_op_code(data)
            seq_number = self.packet_type.get_seq_number(data)
            if op_code == OperationCodes.NSQ_ACK and self.valid_opposite_address(
                address
            ):
                self.logger.debug(f"Received nsq ack with seq_number {seq_number}")
                return

    def receive_response(self, expected_op_code):
        if expected_op_code is None:
            raise Exception("Expected op_code must be specified")
        if expected_op_code == OperationCodes.SV_INTRODUCTION:
            return self.receive_sv_information()
        if expected_op_code == OperationCodes.ACK:
            return self.receive_ack()
        if expected_op_code == OperationCodes.NSQ_ACK:
            return self.receive_nsq_ack()
        if expected_op_code == OperationCodes.END_ACK:
            return self.receive_end_ack()

    #############################
    #     HANDSHAKE METHODS     #
    #############################

    def serialize_information(self, port=None, file_size=None):
        if file_size is None:
            return str(port).encode()
        if not port:
            return str(file_size).encode()
        return f"{port}#{file_size}".encode()

    def send_sv_information(self, file_size=None):
        self.logger.debug(
            f"Sending server information: port = {self.port}, file_size = {file_size}"
        )
        data = self.serialize_information(self.port, file_size)
        try:
            self._send_and_wait(
                OperationCodes.SV_INTRODUCTION, data, OperationCodes.NSQ_ACK
            )
        except:
            self.logger.debug(
                "Server information not acknowledged. Starting process anyway"
            )

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
        encoded_data = self.serialize_information(file_name)
        response_data = self._send_and_wait(
            OperationCodes.DOWNLOAD, encoded_data, OperationCodes.SV_INTRODUCTION
        )
        self.send_nsq_ack()
        return response_data

    def send_up_request(self, file_name, file_size=None):
        self.logger.debug(
            f"Sending upload request with port {self.port}, file_name {file_name} and file_size {file_size}"
        )
        data = self.serialize_information(file_name, file_size)
        self._send_and_wait(OperationCodes.UPLOAD, data, OperationCodes.SV_INTRODUCTION)
        self.send_nsq_ack()

    #############################
    #       OTHER METHODS       #
    #############################

    @property
    def port(self):
        return self.socket.getsockname()[1]

    def valid_opposite_address(self, address):
        return address == self.opposite_address

    def set_timeout(self, timeout):
        self.socket.settimeout(timeout)

    #############################
    #     ABSTRACT METHODS      #
    #############################

    def send_data(self, message):
        raise NotImplementedError

    def receive_data(self, message):
        raise NotImplementedError

    def send_ack(self, message):
        raise NotImplementedError

    def update_seq_number(self):
        raise NotImplementedError

    def valid_packet(self):
        raise NotImplementedError
