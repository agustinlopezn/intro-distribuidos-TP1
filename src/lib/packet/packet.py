class Packet:
    __abstract__ = True

    @staticmethod
    def generate_packet(self, **kwargs):
        raise NotImplementedError

    @staticmethod
    def parse_packet(self, packet):
        raise NotImplementedError

    @staticmethod
    def get_op_code(data):
        raise NotImplementedError

    @staticmethod
    def create_server_information(port):
        raise NotImplementedError
