from .gbn_socket import GBNSocket


class SaWSocket(GBNSocket):
    RWND = 1

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
