from random import random
from lib.packet.saw_packet import SaWPacket
from .custom_socket import CustomSocket, timeout
from lib.protocol_handler import OperationCodes

DROP_PROBABILITY = 0.1


def drop_packet():
    return random() < DROP_PROBABILITY


class SaWSocket(CustomSocket):
    def __init__(self, **kwargs):
        self.seq_number = 0
        super().__init__(**kwargs)

    def _send(self, packet):
        print(
            f"Sending packet with op_code {packet[0]} and seq_number {packet[1]} from port {self.port}"
        )
        if drop_packet():
            print(
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
        print(f"Sending download request with port {self.port}, file_name {file_name}")
        packet = self.generate_packet(
            op_code=OperationCodes.DOWNLOAD, data=file_name.encode()
        )
        return self._send(packet)

    def send_up_request(self, file_name, file_size=None):
        print(
            f"Sending upload request with port {self.port}, file_name {file_name} and file_size {file_size}"
        )
        data = self.serialize_information(file_name, file_size)
        packet = self.generate_packet(op_code=OperationCodes.UPLOAD, data=data)
        self._send(packet)

    def send_sv_information(self, file_size=None):
        print(
            f"Sending server information: port = {self.port}, file_size = {file_size}"
        )
        data = self.serialize_information(self.port, file_size)
        self._send_and_wait(OperationCodes.SV_INTRODUCTION, data)

    def send_ack(self, inverted_seq_number=False):
        packet = SaWPacket.generate_packet(
            op_code=OperationCodes.ACK, seq_number=self.seq_number, data="".encode()
        )
        self._send(packet)

    def send_data(self, data):
        op_code = OperationCodes.DATA
        max_packet_size = SaWPacket.MAX_PAYLOAD_SIZE
        print(f"Sending {len(data)} bytes")
        for head in range(0, len(data), max_packet_size):
            payload = data[head : head + max_packet_size]
            self._send_and_wait(op_code, payload)
            print(f"{len(payload)} bytes sent")

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
                print("Received ack with seq_number", seq_number)
                self.seq_number += 1
                return data

    def receive_data(self):
        while True:
            try:
                data, address = self.socket.recvfrom(SaWPacket.MAX_PACKET_SIZE)
                op_code, seq_number, data = SaWPacket.parse_packet(data)
                print(
                    f"[DATA] Received packet with seq_number {seq_number} and op_code {op_code}"
                )
                if op_code == OperationCodes.DATA:
                    if self.valid_packet(address, seq_number):
                        self.send_ack()
                        self.seq_number += 1
                        return data, True
                    else:  # duplicate packet, should discard and send inverted ack
                        print(f"Received duplicate packet with seq_number {seq_number}")
                        self.seq_number -= 1
                        self.send_ack(inverted_seq_number=True)
                        self.seq_number += 1
                        return data, False
            except timeout:
                pass # shouldn't throw an exception, should just keep iterating

    def receive_sv_information(self):
        while True:
            data, address = self.socket.recvfrom(SaWPacket.MAX_PACKET_SIZE)
            op_code, seq_number, data = SaWPacket.parse_packet(data)
            if op_code == OperationCodes.SV_INTRODUCTION:
                print(f"Received server information: {data}")
                self.opposite_address = address
                return data

    def receive_first_connection(self):
        msg, client_address = self.socket.recvfrom(SaWPacket.MAX_PACKET_SIZE)
        op_code = SaWPacket.get_op_code(msg)
        print(f"Receiving first connection from client at port: {client_address[1]}")
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
        attemps = 3
        packet = self.generate_packet(op_code, data)
        while attemps > 0:
            try:
                self._send(packet)
                data = self.receive_ack()
                return data
            except timeout:
                attemps -= 1
                print("TIMEOUT! Retrying...")
        raise Exception("Connection timed out")

    def close_connection(self):
        self.socket.close()
        print("Connection closed successfully")
