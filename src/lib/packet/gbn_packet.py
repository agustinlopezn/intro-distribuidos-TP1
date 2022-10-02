from .packet import Packet
from src.lib.operation_codes import OperationCodes


import socket
import sys


class GBNPacket(Packet):
    MAX_PAYLOAD_SIZE = 1024
    HEADER_SIZE = 2
    MAX_PACKET_SIZE = HEADER_SIZE + MAX_PAYLOAD_SIZE

    @classmethod
    def generate_packet(cls, op_code, seq_number, data=b""):
        seq_number = 2 ** 8 - 1 if seq_number == -1 else seq_number
        bytes = bytearray(cls.HEADER_SIZE + len(data))
        bytes[0] = op_code
        if seq_number < 0:
            import pdb

            pdb.set_trace()
        bytes[1] = seq_number  # need a more generic name
        bytes[cls.HEADER_SIZE :] = data
        return bytes

    @classmethod
    def parse_packet(cls, packet):
        op_code = packet[0]
        seq_number = packet[1]
        seq_number = -1 if seq_number == 2 ** 8 - 1 else seq_number
        data = packet[cls.HEADER_SIZE :]
        return op_code, seq_number, data

    @classmethod
    def get_packet_data(cls, packet):
        return packet[cls.HEADER_SIZE :]

    @classmethod
    def get_op_code(cls, data):
        try:
            return int(cls.parse_packet(data)[0])
        except ValueError:
            return -1

    @classmethod
    def get_seq_number(cls, data):
        try:
            return int(cls.parse_packet(data)[1])
        except ValueError:
            return -2
