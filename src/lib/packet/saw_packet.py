from .packet import Packet
from src.lib.operation_codes import OperationCodes
import socket


class SaWPacket(Packet):
    MAX_PAYLOAD_SIZE = 1024
    HEADER_SIZE = 2
    MAX_PACKET_SIZE = HEADER_SIZE + MAX_PAYLOAD_SIZE

    @classmethod
    def determine_seq_number(self, bytes_seq_number):
        return int(bytes_seq_number[0])  # esto es horrible, no tiene sentido

    @classmethod
    def generate_packet(cls, op_code, seq_number, data=b""):
        bytes = bytearray(cls.HEADER_SIZE + len(data))
        bytes[0] = op_code
        bytes[1] = seq_number  # need a more generic name
        bytes[cls.HEADER_SIZE :] = data
        return bytes

    @classmethod
    def parse_packet(cls, packet):
        op_code = packet[
        seq_number = packet[1]
        data = packet[cls.HEADER_SIZE :]
        return op_code, seq_number, data

    @classmethod
    def create_server_information(cls, port):
        return cls.generate_packet(
            OperationCodes.SV_INTRODUCTION, 0, 0, str(port).encode()
        )

    @classmethod
    def get_packet_data(cls, packet):
        return packet[cls.HEADER_SIZE :]

    @staticmethod
    def get_op_code(data):
        try:
            return int(SaWPacket.parse_packet(data)[0])
        except ValueError:
            return -1
