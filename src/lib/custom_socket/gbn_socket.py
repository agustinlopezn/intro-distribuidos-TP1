from src.lib.operation_codes import OperationCodes
from src.lib.packet.gbn_packet import GBNPacket

from .custom_socket import CustomSocket, timeout


class GBNSocket(CustomSocket):
    RWND = 20
    MAX_ATTEMPS = 25
    TIMEOUT = 10 / 1000
    MAX_RECEVING_TIME = (MAX_ATTEMPS * TIMEOUT + TIMEOUT) * 3
    # max time to wait for data, then it breaks the connection

    def __init__(self, **kwargs):
        super().__init__(seq_number=-1, packet_type=GBNPacket, **kwargs)
        self.chunk_number = 0

    def send_ack(self):
        packet = GBNPacket.generate_packet(
            op_code=OperationCodes.ACK,
            seq_number=self.seq_number,
            chunk_number=self.chunk_number,
            data="".encode(),
        )
        self._send(packet)

    def generate_packet(self, op_code, data=b""):
        packet = self.packet_type.generate_packet(
            op_code=op_code,
            seq_number=self.seq_number,
            chunk_number=self.chunk_number,
            data=data,
        )
        return packet

    def consecutive_seq_number(self, seq_number):
        # seq_number must be last acked + 1
        return seq_number == self.seq_number + 1

    def update_seq_number(self):
        self.seq_number += 1

    def send_end_ack(self, end_chunk_number=None):
        chunk_number = end_chunk_number or self.chunk_number
        package = self.packet_type.generate_packet(
            op_code=OperationCodes.END_ACK,
            seq_number=self.seq_number,
            chunk_number=chunk_number,
            data="".encode(),
        )
        self._send(package)

    def receive_sv_information(self):
        while True:
            data, address = self.socket.recvfrom(self.packet_type.MAX_PACKET_SIZE)
            (
                op_code,
                seq_number,
                chunk_number,
                parsed_data,
            ) = self.packet_type.parse_packet(data)
            if op_code == OperationCodes.SV_INTRODUCTION:
                self.logger.debug(f"Received server information: {parsed_data}")
                self.opposite_address = address
                return parsed_data

    def receive_data(self):
        self.chunk_number += 1
        self.logger.debug(f"Receiving chunk {self.chunk_number}")
        packages = []
        self.seq_number = -1
        self.set_timeout(self.MAX_RECEVING_TIME)
        while True:
            data, address = self.socket.recvfrom(GBNPacket.MAX_PACKET_SIZE)
            op_code, seq_number, chunk_number, data = GBNPacket.parse_packet(data)
            self.logger.debug(
                f"[DATA] Received packet from port {address[1]} with seq_number {seq_number} and op_code {OperationCodes.op_name(op_code)} from chunk {chunk_number}"
            )
            if chunk_number != self.chunk_number:
                if op_code == OperationCodes.END:
                    self.logger.debug(
                        f"Received END packet from previous chunk: {chunk_number}. Sending end ack for that chunk"
                    )
                    self.send_end_ack(chunk_number)
                    continue
                self.logger.debug(
                    f"Discarding packet with op_code {OperationCodes.op_name(op_code)} and seq_number {self.seq_number} from older chunk: {chunk_number}"
                )
                continue
            if op_code == OperationCodes.DATA:
                if self.consecutive_seq_number(seq_number):
                    self.update_seq_number()
                    self.send_ack()
                    packages.append(data)
                else:
                    self.send_ack()
            elif op_code == OperationCodes.END:
                self.send_end_ack()
                break
        return b"".join(packages)

    def send_end(self):
        self._send_and_wait(OperationCodes.END, "".encode(), OperationCodes.END_ACK)

    def valid_chunk_number(self, chunk_number):
        return chunk_number == self.chunk_number

    def send_data(self, data):
        self.chunk_number += 1
        self.logger.debug(f"Sending chunk {self.chunk_number}")
        self.attemps = self.MAX_ATTEMPS
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
                self.attemps -= 1
                if self.attemps == 0:
                    self.logger.error("Receiver not responding, closing connection")
                    raise Exception  # should be more specific exception
                self.logger.warning(f"Handling timeout...")
                self.last_packet_sent = self.last_packet_acked
                self.logger.debug(f"Last packet sent: {self.last_packet_sent}")
        self.logger.info("All payloads were acked")
        self.send_end()

    def wait_ack(self):
        self.logger.debug(f"Waiting for ack")
        data, address = self.socket.recvfrom(GBNPacket.HEADER_SIZE)
        op_code, ack_number, chunk_number, _data = GBNPacket.parse_packet(data)
        if chunk_number != self.chunk_number:
            self.logger.debug(
                f"Discarding packet with op_code {OperationCodes.op_name(op_code)} and seq_number {ack_number} from older chunk: {chunk_number}"
            )
            return

        if op_code == OperationCodes.ACK and self.valid_opposite_address(address):
            self.attemps = self.MAX_ATTEMPS
            # restarting timeout counter bc receiver is alive
            if (
                ack_number > self.last_packet_acked
                and ack_number <= self.last_packet_sent
            ):
                self.logger.debug(f"Updating last packet acked to {ack_number}")
                self.last_packet_acked = ack_number
        else:
            self.logger.debug(
                f"Received and discarded packet with op_code {OperationCodes.op_name(op_code)}"
            )

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
            self.send_data_packet(payload)
            self.last_packet_sent += 1
            packets_in_traffic += 1

    def send_data_packet(self, payload):
        packet = self.packet_type.generate_packet(
            op_code=OperationCodes.DATA,
            seq_number=self.last_packet_sent + 1,
            chunk_number=self.chunk_number,
            data=payload,
        )
        self._send(packet)

    def valid_packet(self, address, seq_number):
        return self.valid_opposite_address(address)

    def close_connection(self, confirm_close=False):
        self.socket.close()
        self.logger.info("Connection closed successfully")

    def receive_end_ack(self):
        while True:
            data, address = self.socket.recvfrom(self.packet_type.MAX_PACKET_SIZE)
            op_code, seq_number, chunk_number, data = self.packet_type.parse_packet(
                data
            )
            if (
                op_code == OperationCodes.END_ACK
                and self.valid_opposite_address(address)
                and self.valid_chunk_number(chunk_number)
            ):
                self.logger.debug(f"Received nsq ack with seq_number {seq_number}")
                return
