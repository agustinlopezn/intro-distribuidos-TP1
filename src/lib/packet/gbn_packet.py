from .packet import Packet
from src.lib.operation_codes import OperationCodes


import socket
import sys


class GBNPacket(Packet):
    MAX_PAYLOAD_SIZE = 1024
    HEADER_SIZE = 4
    MAX_PACKET_SIZE = HEADER_SIZE + MAX_PAYLOAD_SIZE

    @classmethod
    def generate_packet(cls, op_code, seq_number, chunk_number, data=b""):
        seq_number = 2 ** 8 - 1 if seq_number == -1 else seq_number
        new_chunk_number = socket.htons(chunk_number)
        try:
            chunk_seq_number = new_chunk_number.to_bytes(2, byteorder="big")
        except Exception as e:
            import pdb; pdb.set_trace()
        bytes = bytearray(cls.HEADER_SIZE + len(data))
        bytes[0] = op_code
        bytes[1] = seq_number  # need a more generic name
        bytes[2:4] = chunk_seq_number
        bytes[cls.HEADER_SIZE :] = data
        return bytes

    @classmethod
    def parse_packet(cls, packet):
        op_code = packet[0]
        seq_number = packet[1]
        seq_number = -1 if seq_number == 2 ** 8 - 1 else seq_number
        bytes_chunk_number = packet[2:4]
        chunk_number = int.from_bytes(bytes_chunk_number, byteorder="big", signed=False)
        chunk_number = socket.ntohs(chunk_number)
        data = packet[cls.HEADER_SIZE :]
        return op_code, seq_number, chunk_number, data

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

    @classmethod
    def get_chunk_number(cls, data):
        try:
            chunk_number = int.from_bytes(data[2:4], byteorder="big", signed=False)
            return socket.ntohl(chunk_number)
        except ValueError:
            return -1
