from .packet import Packet
from lib.protocol_handler import OperationCodes


class SaWPacket(Packet):
    MAX_PAYLOAD_SIZE = 1022
    HEADER_SIZE = 2
    MAX_PACKET_SIZE = HEADER_SIZE + MAX_PAYLOAD_SIZE 

    @classmethod
    def generate_packet(cls, op_code, seq_number, data):
        bytes = bytearray(cls.HEADER_SIZE + len(data))
        bytes[0] = op_code
        bytes[1] = seq_number # need a more generic name
        bytes[2:] = data
        return bytes

    @staticmethod
    def parse_packet(packet):
        op_code = packet[0]
        seq_number = packet[1]
        data = packet[2:]
        return op_code, seq_number, data

    @staticmethod
    def create_server_information(port):
        return SaWPacket.generate_packet(
            OperationCodes.SV_INTRODUCTION, 0, 0, str(port).encode()
        )

    @staticmethod
    def get_packet_data(packet):
        return packet[2:]

    @staticmethod
    def get_op_code(data):
        try:
            return int(SaWPacket.parse_packet(data)[0])
        except ValueError:
            return -1
