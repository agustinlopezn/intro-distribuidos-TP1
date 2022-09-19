class Packet:
    __abstract__ = True

    def generate_packet(self):
        pass

    def parse_packet(self):
        pass

    @staticmethod
    def get_op_code(data):
        return int(data[0])