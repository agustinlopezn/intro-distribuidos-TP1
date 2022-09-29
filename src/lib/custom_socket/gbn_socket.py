from random import random
from lib.packet.gbn_packet import GBNPacket
from .custom_socket import CustomSocket, timeout
from lib.protocol_handler import OperationCodes

DROP_PROBABILITY = 0


def drop_packet():
    return random() < DROP_PROBABILITY


class GBNSocket(CustomSocket):
    RWND = 2
    MAX_ATTEMPS = 5

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def _send(self, packet):
        self.logger.debug(
            f"Sending packet with op_code {packet[0]} and seq_number {packet[1]} from port {self.port}"
        )
        if drop_packet():
            self.logger.debug(
                f"Dropping packet with op_code {packet[0]} and seq_number {packet[1]}"
            )
            return
        self.socket.sendto(packet, self.opposite_address)

    def generate_packet(self, op_code, data):
        packet = GBNPacket.generate_packet(
            op_code=op_code, seq_number=self.seq_number, data=data
        )
        return packet

    def send_nsq_ack(self):
        packet = self.generate_packet(op_code=OperationCodes.NSQ_ACK, data="".encode())
        self._send(packet)

    def serialize_information(self, port, file_size):
        if not file_size:
            return str(port).encode()
        if not port:
            return str(file_size).encode()
        return f"{port}#{file_size}".encode()

    def send_dl_request(self, file_name):
        self.logger.debug(
            f"Sending download request with port {self.port}, file_name {file_name}"
        )
        packet = self.generate_packet(
            op_code=OperationCodes.DOWNLOAD, data=file_name.encode()
        )
        return self._send(packet)

    def send_up_request(self, file_name, file_size=None):
        self.logger.debug(
            f"Sending upload request with port {self.port}, file_name {file_name} and file_size {file_size}"
        )
        data = self.serialize_information(file_name, file_size)
        packet = self.generate_packet(op_code=OperationCodes.UPLOAD, data=data)
        self._send(packet)

    def send_sv_information(self, file_size=None):
        self.logger.debug(
            f"Sending server information: port = {self.port}, file_size = {file_size}"
        )
        data = self.serialize_information(self.port, file_size)
        try:
            self._send_and_wait(OperationCodes.SV_INTRODUCTION, data)
        except:
            self.logger.debug(
                "Server information not acknowledged. Starting process anyway"
            )

    def send_ack(self):
        packet = GBNPacket.generate_packet(
            op_code=OperationCodes.ACK, seq_number=self.seq_number, data="".encode()
        )
        self._send(packet)

    def consecutive_seq_number(self, seq_number):
        # seq_number must be last acked + 1
        return seq_number == self.seq_number + 1

    def update_sequence_number(self):
        self.seq_number += 1

    def receive_data(self):
        packages = []
        self.seq_number = -1
        while True:
            self.socket.settimeout(None)
            data, address = self.socket.recvfrom(GBNPacket.MAX_PACKET_SIZE)
            op_code, seq_number, data = GBNPacket.parse_packet(data)
            self.logger.debug(
                f"[DATA] Received packet from port {address[1]} with seq_number {seq_number} and op_code {op_code}"
            )
            if op_code == OperationCodes.DATA:
                if self.consecutive_seq_number(seq_number):
                    self.update_sequence_number()
                    self.send_ack()
                    packages.append(data)
                else:
                    self.send_ack()
            elif op_code == OperationCodes.END:
                for i in range(self.MAX_ATTEMPS):
                    self.send_nsq_ack()
                break
        return b"".join(packages)
        
    def send_end(self):
        self._send_and_wait(OperationCodes.END, "".encode())

    def send_data(self, data):
        self.last_packet_sent = -1
        self.last_packet_acked = -1
        max_packet_size = GBNPacket.MAX_PAYLOAD_SIZE
        self.payloads = []
        for head in range(0, len(data), max_packet_size):
            payload = data[head : head + max_packet_size]
            self.payloads.append(payload)
        self.logger.debug(f"Sending {len(self.payloads)} packets")
        while self.last_packet_acked < len(self.payloads) - 1:
            self.try_to_send_packets()
            try:
                self.wait_ack()
            except timeout:
                self.logger.debug(f"Handling timeout...")
                self.last_packet_sent = self.last_packet_acked
                self.logger.debug(f"Last packet sent: {self.last_packet_sent}")
        self.logger.info("All payloads were acked")
        self.send_end()

    def handle_timeout(self):
        self.logger.debug(f"Handling timeout...")
        packets_sent_but_not_acked = self.last_packet_sent - self.last_packet_acked
        packets_to_resend = min(packets_sent_but_not_acked, self.RWND)
        self.logger.debug(f"Packets to resend: {packets_to_resend}")
        starting_index = self.last_packet_acked + 1
        ending_index = starting_index + packets_to_resend
        for i in range(starting_index, ending_index):
            payload = self.payloads[i]
            self.send_packet(payload)

    def wait_ack(self):
        self.logger.debug(f"Waiting for ack")
        self.socket.settimeout(10)
        data, address = self.socket.recvfrom(GBNPacket.HEADER_SIZE)
        op_code, ack_number, _data = GBNPacket.parse_packet(data)

        if op_code == OperationCodes.ACK and self.valid_opposite_address(address):
            if ack_number > self.last_packet_acked:
                self.logger.debug(f"Updating last packet acked to {ack_number}")
                self.last_packet_acked = ack_number

    def try_to_send_packets(self):
        self.logger.debug(f"Trying to send packages...")
        self.logger.debug(f"Last packet sent: {self.last_packet_sent}")
        self.logger.debug(f"Last packet acked: {self.last_packet_acked}")
        packets_in_traffic = self.last_packet_sent - self.last_packet_acked
        self.logger.debug(f"Packets in traffic: {packets_in_traffic}")
        while self.RWND > packets_in_traffic:
            if self.last_packet_sent == len(self.payloads) - 1:
                break
            payload = self.payloads[self.last_packet_sent + 1]
            self.logger.debug(f"Sending packet {self.last_packet_sent + 1} ")
            self.send_packet(payload)
            self.last_packet_sent += 1
            packets_in_traffic += 1

    def send_packet(self, payload):
        packet = GBNPacket.generate_packet(
            op_code=OperationCodes.DATA,
            seq_number=self.last_packet_sent + 1,
            data=payload,
        )
        self._send(packet)

    def valid_seq_number(self, received_seq_number):
        return received_seq_number == self.seq_number

    def receive_ack(self):
        while True:
            data, address = self.socket.recvfrom(GBNPacket.MAX_PACKET_SIZE)
            op_code, seq_number, data = GBNPacket.parse_packet(data)
            if op_code == OperationCodes.NSQ_ACK and self.valid_opposite_address(
                address
            ):
                return data
            if op_code == OperationCodes.ACK and self.valid_opposite_address(address):
                self.logger.debug(f"Received ack with seq_number {seq_number}")
                self.update_sequence_number()
                return data

    def receive_sv_information(self):
        while True:
            data, address = self.socket.recvfrom(GBNPacket.MAX_PACKET_SIZE)
            op_code, seq_number, data = GBNPacket.parse_packet(data)
            if op_code == OperationCodes.SV_INTRODUCTION:
                self.logger.debug(f"Received server information: {data}")
                self.opposite_address = address
                return data

    def receive_first_connection(self):
        msg, client_address = self.socket.recvfrom(GBNPacket.MAX_PACKET_SIZE)
        op_code = GBNPacket.get_op_code(msg)
        self.logger.debug(
            f"Receiving first connection from client at port: {client_address[1]}"
        )
        if op_code not in (OperationCodes.DOWNLOAD, OperationCodes.UPLOAD):
            raise Exception("Invalid operation code")
        return op_code, client_address, GBNPacket.get_packet_data(msg).decode()

    def valid_opposite_address(self, address):
        return address == self.opposite_address

    def valid_packet(self, address, seq_number):
        return self.valid_opposite_address(address) and self.valid_seq_number(
            seq_number
        )

    def _send_and_wait(self, op_code, data):
        attemps = self.MAX_ATTEMPS
        packet = self.generate_packet(op_code, data)
        while attemps > 0:
            try:
                self._send(packet)
                self.receive_ack()
                return
            except timeout:
                attemps -= 1
                self.logger.warning("TIMEOUT! Retrying...")
        raise Exception("Connection timed out")

    def close_connection(self):
        self.socket.close()
        self.logger.info("Connection closed successfully")
