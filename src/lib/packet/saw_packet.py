from .packet import Packet


class SaWPacket(Packet):

    @staticmethod
    def generate_packet(data):
        raise NotImplementedError

    @staticmethod
    def parse_packet(packet):
        packet = packet.decode()
        op_code = packet[0]
        data = packet[1:]
        return op_code, data
