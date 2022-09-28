from random import random
from lib.packet.saw_packet import SaWPacket
from .custom_socket import CustomSocket, timeout
from lib.protocol_handler import OperationCodes

DROP_PROBABILITY = 0.0


def drop_packet():
    return random() < DROP_PROBABILITY


class SaWSocket(CustomSocket):
    def __init__(self, **kwargs):
        self.seq_number = 0
        super().__init__(**kwargs)

    def _send(self, packet):
        self.logger.debug(
            f"Sending packet with op_code {packet[0]} and seq_number {packet[1]} from port {self.port}"
        )
        if drop_packet():
            self.logger.debug(
                f"Dropping packet with op_code {packet[0]} and seq_number {packet[1]}"
            )
            return
        self.socket.sendto(packet, self.opposite_address)

    def generate_packet(self, op_code, data):
        packet = SaWPacket.generate_packet(
            op_code=op_code, seq_number=self.seq_number, data=data
        )
        return packet

    def send_nsq_ack(self):
        packet = self.generate_packet(op_code=OperationCodes.NSQ_ACK, data="".encode())
        self._send(packet)

    def serialize_information(self, port, file_size):
        if not file_size:
            return str(port).encode()
        if not port:
            return str(file_size).encode()
        return f"{port}#{file_size}".encode()

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

    def send_sv_information(self, file_size=None):
        self.logger.debug(
            f"Sending server information: port = {self.port}, file_size = {file_size}"
        )
        data = self.serialize_information(self.port, file_size)
        try:
            self._send_and_wait(OperationCodes.SV_INTRODUCTION, data)
        except:
            self.logger.debug(
                "Server information not acknowledged. Starting process anyway"
            )

    def send_ack(self):
        packet = SaWPacket.generate_packet(
            op_code=OperationCodes.ACK, seq_number=self.seq_number, data="".encode()
        )
        self._send(packet)

    def send_data(self, data):
        op_code = OperationCodes.DATA
        max_packet_size = SaWPacket.MAX_PAYLOAD_SIZE
        self.logger.debug(f"Sending {len(data)} bytes")
        for head in range(0, len(data), max_packet_size):
            payload = data[head : head + max_packet_size]
            self._send_and_wait(op_code, payload)
            self.logger.debug(f"{len(payload)} bytes sent")

    def valid_seq_number(self, received_seq_number):
        return received_seq_number == self.seq_number

    def receive_ack(self):
        while True:
            data, address = self.socket.recvfrom(SaWPacket.MAX_PACKET_SIZE)
            op_code, seq_number, data = SaWPacket.parse_packet(data)
            if op_code == OperationCodes.NSQ_ACK and self.valid_opposite_address(
                address
            ):
                return data
            if op_code == OperationCodes.ACK and self.valid_packet(address, seq_number):
                self.logger.debug(f"Received ack with seq_number {seq_number}")
                self.update_sequence_number()
                return data

    def update_sequence_number(self):
        self.seq_number = int(not self.seq_number)
        # self.seq_number += 1 # this way is better for debugging

    def receive_data(self):
        while True:
            try:
                data, address = self.socket.recvfrom(SaWPacket.MAX_PACKET_SIZE)
                op_code, seq_number, data = SaWPacket.parse_packet(data)
                self.logger.debug(
                    f"[DATA] Received packet from port {address[1]} with seq_number {seq_number} and op_code {op_code}"
                )
                if op_code == OperationCodes.DATA:
                    if self.valid_packet(address, seq_number):
                        self.send_ack()
                        correct_data = True  # received data is correct
                    else:  # duplicate packet, should discard and send inverted ack
                        self.logger.warning(
                            f"Received duplicate packet with seq_number {seq_number}"
                        )
                        self.update_sequence_number()  # ack belongs to previous packet
                        self.send_ack()
                        correct_data = (
                            False
                        )  # received data belongs to a previous packet
                    self.update_sequence_number()
                    return data, correct_data
            except timeout:
                pass  # shouldn't throw an exception, should just keep iterating

    def receive_sv_information(self):
        while True:
            data, address = self.socket.recvfrom(SaWPacket.MAX_PACKET_SIZE)
            op_code, seq_number, data = SaWPacket.parse_packet(data)
            if op_code == OperationCodes.SV_INTRODUCTION:
                self.logger.debug(f"Received server information: {data}")
                self.opposite_address = address
                return data

    def receive_first_connection(self):
        msg, client_address = self.socket.recvfrom(SaWPacket.MAX_PACKET_SIZE)
        op_code = SaWPacket.get_op_code(msg)
        self.logger.debug(
            f"Receiving first connection from client at port: {client_address[1]}"
        )
        if op_code not in (OperationCodes.DOWNLOAD, OperationCodes.UPLOAD):
            raise Exception("Invalid operation code")
        return op_code, client_address, SaWPacket.get_packet_data(msg).decode()

    def valid_opposite_address(self, address):
        return address == self.opposite_address

    def valid_packet(self, address, seq_number):
        return self.valid_opposite_address(address) and self.valid_seq_number(
            seq_number
        )

    def _send_and_wait(self, op_code, data):
        attemps = 5
        packet = self.generate_packet(op_code, data)
        while attemps > 0:
            try:
                self._send(packet)
                data = self.receive_ack()
                return data
            except timeout:
                attemps -= 1
                self.logger.warning("TIMEOUT! Retrying...")
        raise Exception("Connection timed out")

    def close_connection(self):
        self.socket.close()
        self.logger.info("Connection closed successfully")
