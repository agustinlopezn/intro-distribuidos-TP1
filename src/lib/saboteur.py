from random import random
from threading import Thread
import time
from src.lib.operation_codes import OperationCodes

DELAY_PROBABILITY = 0
DROP_PROBABILITY = 0.2
DUPLICATION_PROBABILITY = 0


class Delayer(Thread):
    DELAY_TIME = 5 / 1000

    def __init__(self, function, packet, logger):
        super().__init__()
        self.function = function
        self.packet = packet
        self.logger = logger

    def run(self):
        try:
            time.sleep(self.DELAY_TIME)
            self.function(self.packet)
        except OSError:
            self.logger.warning(
                "Delayer not resending packet because the socket is closed"
            )


class Dropper:
    @staticmethod
    def drop_packet():
        pass


class Duplicator:
    @staticmethod
    def duplicate_packet(send_function, packet):
        send_function(packet)
        send_function(packet)


class Saboteur:
    def __init__(self, send_function, packet_type, logger):
        self.send_function = send_function
        self.logger = logger
        self.packet_type = packet_type

    def sabotage_packet(self, packet):
        op_code = packet[0]
        seq_number = self.packet_type.get_seq_number(packet)
        if random() < DELAY_PROBABILITY:
            Delayer(self.send_function, packet, self.logger).start()
            self.logger.warning(
                f"Packet with op_code {OperationCodes.op_name(op_code)} and seq_number {seq_number} was delayed"
            )
            return True
        if random() < DROP_PROBABILITY:
            self.logger.warning(
                f"Packet with op_code {OperationCodes.op_name(op_code)} and seq_number {seq_number} was dropped"
            )
            Dropper.drop_packet()  # literally does nothing
            return True
        if random() < DUPLICATION_PROBABILITY:
            self.logger.warning(
                f"Packet with op_code {OperationCodes.op_name(op_code)} and seq_number {seq_number} was duplicated"
            )
            Duplicator.duplicate_packet(self.send_function, packet)
            return True
        return False


class NullSaboteur:
    def __init__(self, **kwargs):
        pass

    def sabotage_packet(self, packet):
        return False
