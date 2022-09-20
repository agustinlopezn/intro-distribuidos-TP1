from lib.packet.saw_packet import SaWPacket
from .custom_socket import CustomSocket, timeout
from lib.protocol_handler import OperationCodes


class SaWSocket(CustomSocket):
    def __init__(self, client_address, timeout):
        super().__init__(client_address, packet_type=SaWPacket, timeout=timeout)

    def _send(self, packet):
        b_s = self.socket.sendto(packet, self.client_address)
        return b_s

    def send_dl_request(self):
        packet = self.packet_type.generate_packet(
            op_code=OperationCodes.DOWNLOAD,
            seq_number=0,
            ack_number=0,
            data="".encode(),
        )
        self._send(packet)

    def send_cl_information(self, data):
        packet = self.packet_type.generate_packet(
            op_code=OperationCodes.CL_INFORMATION,
            seq_number=0,
            ack_number=0,
            data=data.encode(),
        )
        self._send(packet)

    def send_up_request(self):
        packet = self.packet_type.generate_packet(
            op_code=OperationCodes.UPLOAD,
            seq_number=0,
            ack_number=0,
            data="".encode()
        )
        self._send(packet)

    def send_end(self):
        packet = self.packet_type.generate_packet(
            op_code=OperationCodes.END,
            seq_number=0,
            ack_number=0,
            data="".encode()
        )
        self._send(packet)

    def send_sv_information(self, port):
        packet = self.packet_type.generate_packet(
            op_code=OperationCodes.SV_INFORMATION,
            seq_number=0,
            ack_number=0,
            data=str(port).encode(),
        )
        self._send(packet)

    def send_ack(self):
        packet = self.packet_type.generate_packet(
            op_code=OperationCodes.ACK,
            seq_number=0,
            ack_number=0,
            data="".encode(),
        )
        self._send(packet)

    def send_data(self, data):
        attemps = 3
        while attemps > 0:
            try:
                packet = self.packet_type.generate_packet(
                    op_code=OperationCodes.DATA,
                    seq_number=0,
                    ack_number=0,
                    data=data,
                )
                self._send(packet)
                op_code, seq_number, ack_number, data = self.receive()
                if op_code == OperationCodes.ACK:
                    return
                raise timeout
            except timeout:
                attemps -= 1
                print("TIMEOUT! Retrying...")
        raise Exception("Connection timed out")

    def receive(self):
        data, address = self.socket.recvfrom(1024)
        return self.packet_type.parse_packet(data)
