from .custom_socket import CustomSocket, timeout


class SaWSocket(CustomSocket):
    def _send(self, message):
        b_s = self.socket.sendto(message, self.client_address)
        return b_s

    def send(self, message):
        attemps = 3
        while attemps > 0:
            try:
                self._send(message)
                data, address = self.socket.recvfrom(1024)
                # Parse data and check SEQ number matchs
                return
            except timeout:
                attemps -= 1
                print("TIMEOUT! Retrying...")
        raise Exception("Connection timed out")

    def receive(self):
        data, address = self.socket.recvfrom(1024)
        return self.packet_type.parse_packet(data)
