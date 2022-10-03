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
    def get_op_code(data):
        raise NotImplementedError

    @classmethod
    def get_packet_data(cls, packet):
        return packet[cls.HEADER_SIZE :]
