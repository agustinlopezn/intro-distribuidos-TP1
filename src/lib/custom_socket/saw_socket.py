from re import S
from src.lib.packet.saw_packet import SaWPacket
from .custom_socket import CustomSocket, timeout
from src.lib.operation_codes import OperationCodes


class SaWSocket(CustomSocket):
    MAX_ATTEMPS = 5
    TIMEOUT = 10 / 1000

    def __init__(self, **kwargs):
        self.seq_number = 0
        self.packet_type = SaWPacket
        super().__init__(**kwargs)

    def generate_packet(self, op_code, data):
        packet = SaWPacket.generate_packet(
            op_code=op_code, seq_number=self.seq_number, data=data
        )
        return packet

    def send_nsq_ack(self):
        packet = self.generate_packet(op_code=OperationCodes.NSQ_ACK, data="".encode())
        self._send(packet)

    def send_ack(self, invert_ack=False):
        # ack_number = int(not self.seq_number) if invert_ack else self.seq_number
        ack_number = self.seq_number - 1 if invert_ack else self.seq_number
        packet = SaWPacket.generate_packet(
            op_code=OperationCodes.ACK, seq_number=ack_number, data="".encode()
        )
        self._send(packet)

    def send_data(self, data):
        op_code = OperationCodes.DATA
        max_packet_size = SaWPacket.MAX_PAYLOAD_SIZE
        self.logger.debug(f"Sending {len(data)} bytes")
        for head in range(0, len(data), max_packet_size):
            payload = data[head : head + max_packet_size]
            self._send_and_wait(op_code, payload, OperationCodes.ACK)
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
        # self.seq_number = int(not self.seq_number)
        self.seq_number += 1  # this way is better for debugging

    def receive_data(self):
        while True:
            self.socket.settimeout(None)
            data, address = self.socket.recvfrom(SaWPacket.MAX_PACKET_SIZE)
            op_code, seq_number, data = SaWPacket.parse_packet(data)
            self.logger.debug(
                f"[DATA] Received packet from port {address[1]} with seq_number {seq_number} and op_code {OperationCodes.op_name(op_code)}"
            )
            if op_code == OperationCodes.DATA and self.valid_opposite_address(address):
                if self.valid_seq_number(seq_number):
                    self.send_ack()
                    self.update_sequence_number()
                    return data
                else:  # duplicate packet, should discard and send inverted ack
                    self.logger.warning(
                        f"Received duplicate packet with seq_number {seq_number} and op_code {OperationCodes.op_name(op_code)}"
                    )
                    self.send_ack(invert_ack=True)

    def valid_opposite_address(self, address):
        return address == self.opposite_address

    def valid_packet(self, address, seq_number):
        return self.valid_opposite_address(address) and self.valid_seq_number(
            seq_number
        )

    def close_connection(self):
        self.socket.close()
        self.logger.info("Connection closed successfully")
