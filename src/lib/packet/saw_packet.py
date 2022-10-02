from .packet import Packet
from src.lib.operation_codes import OperationCodes
import socket


class SaWPacket(Packet):
    MAX_PAYLOAD_SIZE = 1024
    HEADER_SIZE = 2
    MAX_PACKET_SIZE = HEADER_SIZE + MAX_PAYLOAD_SIZE

    @classmethod
    def generate_packet(cls, op_code, seq_number, data=b""):
        bytes = bytearray(cls.HEADER_SIZE + len(data))
        bytes[0] = op_code
        bytes[1] = seq_number  # need a more generic name
        bytes[cls.HEADER_SIZE :] = data
        return bytes

    @classmethod
    def parse_packet(cls, packet):
        op_code = packet[0]
        seq_number = packet[1]
        data = packet[cls.HEADER_SIZE :]
        return op_code, seq_number, data

    @staticmethod
    def get_op_code(data):
        try:
            return int(SaWPacket.parse_packet(data)[0])
        except ValueError:
            return -1

    @classmethod
    def get_seq_number(cls, data):
        try:
            return int(cls.parse_packet(data)[1])
        except ValueError:
            return -2
