import sys
from socket import *
from src.lib.logger import Logger

from src.lib.custom_socket.saw_socket import SaWSocket
from src.lib.options import DownloadOptions, UploadOptions
from src.lib.file_handler.file_sender.client_file_sender import ClientFileSender
from src.lib.file_handler.file_receiver.client_file_receiver import (
    ClientFileReceiver,
)
from src.lib.operation_codes import OperationCodes


class Client:
    @classmethod
    def upload(cls):
        options = UploadOptions(sys.argv[1:])
        
        if not options.valid():
            print("Error: some options are invalid")
            options.show_help = True
        if options.show_help:
            print("usage: upload [-h] [-v | -q] [-H ADDR] [-p PORT] [-s FILEPATH] [-n FILENAME]")
            return
        logger = Logger("client", options.verbose, options.quiet)
        server_address = (options.host, options.port)
        ClientFileSender(
            options.file_name,
            source_path=options.src,
            logger=logger,
            opposite_address=server_address,
        ).handle_send_process()

    @classmethod
    def download(cls):
        options = DownloadOptions(sys.argv[1:])
        if not options.valid():
            print("Error: some options are invalid")
            options.show_help = True
        if options.show_help:
            print("usage: download [-h] [-v | -q] [-H ADDR] [-p PORT] [-d FILEPATH] [-n FILENAME]")
            return
        logger = Logger("client", options.verbose, options.quiet)
        server_address = (options.host, options.port)
        ClientFileReceiver(
            options.file_name,
            dest_path=options.dst,
            logger=logger,
            opposite_address=server_address,
        ).handle_receive_process()
