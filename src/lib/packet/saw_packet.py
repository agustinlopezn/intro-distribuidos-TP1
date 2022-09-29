from .packet import Packet
from src.lib.protocol_handler import OperationCodes


import socket
import sys


class SaWPacket(Packet):
    MAX_PAYLOAD_SIZE = 1022
    HEADER_SIZE = 5
    MAX_PACKET_SIZE = HEADER_SIZE + MAX_PAYLOAD_SIZE

    @classmethod
    def generate_packet(cls, op_code, seq_number, data):
        seq_number = socket.htonl(seq_number)
        bytes_seq_number = seq_number.to_bytes(4, byteorder="big")
        bytes = bytearray(cls.HEADER_SIZE + len(data))
        bytes[0] = op_code
        bytes[1:5] = bytes_seq_number  # need a more generic name
        bytes[5:] = data
        return bytes

    @staticmethod
    def parse_packet(packet):
        op_code = packet[0]
        bytes_seq_number = packet[1:5]
        seq_number = int.from_bytes(bytes_seq_number, byteorder="big", signed=False)
        seq_number = socket.ntohl(seq_number)
        data = packet[5:]
        return op_code, seq_number, data

    @staticmethod
    def create_server_information(port):
        return SaWPacket.generate_packet(
            OperationCodes.SV_INTRODUCTION, 0, 0, str(port).encode()
        )

    @staticmethod
    def get_packet_data(packet):
        return packet[5:]

    @staticmethod
    def get_op_code(data):
        try:
            return int(SaWPacket.parse_packet(data)[0])
        except ValueError:
            return -1
