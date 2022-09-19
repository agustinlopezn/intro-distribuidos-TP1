from lib.protocol_handler import OperationCodes


class Packet:
    __abstract__ = True

    def generate_packet(self):
        pass

    def parse_packet(self):
        pass

    @staticmethod
    def get_op_code(data):
        return int(data[0])

    @staticmethod
    def create_server_information(port):
        msg = str(OperationCodes.SV_INFORMATION) + str(port)
        return msg.encode()