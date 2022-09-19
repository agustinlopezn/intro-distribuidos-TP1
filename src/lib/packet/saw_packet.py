from .packet import Packet
from lib.protocol_handler import OperationCodes


class SaWPacket(Packet):
    @staticmethod
    def generate_packet(op_code, seq_number, ack_number, data):
        bytes = bytearray(3 + len(data))
        bytes[0] = op_code
        bytes[1] = seq_number
        bytes[2] = ack_number
        bytes[3:] = data
        return bytes

    @staticmethod
    def parse_packet(packet):
        op_code = packet[0]
        seq_number = packet[1]
        ack_number = packet[2]
        data = packet[3:]
        return op_code, seq_number, ack_number, data

    @staticmethod
    def create_server_information(port):
        return SaWPacket.generate_packet(
            OperationCodes.SV_INFORMATION, 0, 0, str(port).encode()
        )

    @staticmethod
    def get_op_code(data):
        try:
            return int(SaWPacket.parse_packet(data)[0])
        except ValueError:
            return -1
