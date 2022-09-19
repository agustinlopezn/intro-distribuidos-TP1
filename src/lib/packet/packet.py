from lib.protocol_handler import OperationCodes


class Packet:
    __abstract__ = True

    @staticmethod
    def generate_packet(self, data):
        raise NotImplementedError

    @staticmethod
    def parse_packet(self, packet):
        raise NotImplementedError

    @staticmethod
    def get_op_code(data):
        return int(data[0])

    @staticmethod
    def create_server_information(port):
        msg = str(OperationCodes.SV_INFORMATION) + str(port)
        return msg.encode()
