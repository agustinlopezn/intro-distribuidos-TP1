class OperationCodes:
    """Operation codes for the protocol"""

    DOWNLOAD = 0
    UPLOAD = 1
    SV_INTRODUCTION = 2
    FILE_INFORMATION = 3
    DATA = 4
    ACK = 5
    ERROR = 6
    END = 7
    NSQ_ACK = 8

    OPERATION_NAMES = [
        "DOWNLOAD",
        "UPLOAD",
        "SV_INTRODUCTION",
        "FILE_INFORMATION",
        "DATA",
        "ACK",
        "ERROR",
        "END",
        "NSQ_ACK"
    ]

    @classmethod
    def op_name(cls, op_code):
        return cls.OPERATION_NAMES[op_code]
