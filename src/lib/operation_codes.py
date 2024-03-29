class OperationCodes:
    """Operation codes for the protocol"""

    DOWNLOAD = 0
    UPLOAD = 1
    SV_INTRODUCTION = 2
    DATA = 3
    ACK = 4
    NSQ_ACK = 5
    END_ACK = 6
    END = 7

    OPERATION_NAMES = [
        "DOWNLOAD",
        "UPLOAD",
        "SV_INTRODUCTION",
        "DATA",
        "ACK",
        "NSQ_ACK",
        "END_ACK",
        "END",
    ]

    @classmethod
    def op_name(cls, op_code):
        return cls.OPERATION_NAMES[op_code]
