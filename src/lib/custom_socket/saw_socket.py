from lib.packet.saw_packet import SaWPacket
from .custom_socket import CustomSocket, timeout
from lib.protocol_handler import OperationCodes


class SaWSocket(CustomSocket):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def _send(self, packet):
        b_s = self.socket.sendto(packet, self.destination_address)
        return b_s

    def send_dl_request(self):
        op_code = OperationCodes.DOWNLOAD
        expected_response_code = OperationCodes.SV_INFORMATION
        return self._send_and_wait(op_code, "".encode(), expected_response_code)

    def send_up_request(self):
        packet = SaWPacket.generate_packet(
            op_code=OperationCodes.UPLOAD, seq_number=0, ack_number=0, data="".encode()
        )
        self._send(packet)

    def send_end(self):
        packet = SaWPacket.generate_packet(
            op_code=OperationCodes.END, seq_number=0, ack_number=0, data="".encode()
        )
        self._send(packet)

    def send_sv_information(self, port):
        packet = SaWPacket.generate_packet(
            op_code=OperationCodes.SV_INFORMATION,
            seq_number=0,
            ack_number=0,
            data=str(port).encode(),
        )
        self._send(packet)

    def send_ack(self):
        packet = SaWPacket.generate_packet(
            op_code=OperationCodes.ACK, seq_number=0, ack_number=0, data="".encode()
        )
        self._send(packet)

    def send_data(self, data):
        op_code = OperationCodes.DATA
        return self._send_and_wait(op_code, data)

    def receive(self):
        data, address = self.socket.recvfrom(1024)
        op_code, seq_number, ack_number, data = SaWPacket.parse_packet(data)
        return op_code, data

    def receive_first_connection(self):
        msg, client_address = self.socket.recvfrom(1024)
        op_code = SaWPacket.get_op_code(msg)
        if op_code not in (OperationCodes.DOWNLOAD, OperationCodes.UPLOAD):
            raise Exception("Invalid operation code")
        return op_code, client_address

    def serialize_file_information(self, file_name, file_size):
        if not file_size:
            return file_name.encode()
        if not file_name:
            return str(file_size).encode()
        return f"{file_name}#{file_size}".encode()

    def send_file_information(self, file_name=None, file_size=None):
        file_information = self.serialize_file_information(file_name, file_size)
        op_code = OperationCodes.FILE_INFORMATION
        expected_response_code = (
            OperationCodes.ACK
            if file_size is not None
            else OperationCodes.FILE_INFORMATION
        )
        return self._send_and_wait(op_code, file_information, expected_response_code)

    def _send_and_wait(self, op_code, data, expected_response_code=OperationCodes.ACK):
        attemps = 3
        while attemps > 0:
            try:
                packet = SaWPacket.generate_packet(
                    op_code=op_code, seq_number=0, ack_number=0, data=data
                )
                self._send(packet)
                rcvd_op_code, data = self.receive()
                if rcvd_op_code == expected_response_code:
                    return data
                raise timeout
            except timeout:
                attemps -= 1
                print("TIMEOUT! Retrying...")
        raise Exception("Connection timed out")

    def close_connection(self, total_bytes, expected_bytes):
        try:
            self.send_end()
            print("Connection closed successfully")
        except Exception as e:
            if total_bytes == expected_bytes:
                print("Data sent/received successfully")
            else:
                print(e)
            print(e)
        finally:
            self.socket.close()
