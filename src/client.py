import sys
from socket import *
from lib.logger import Logger

from lib.custom_socket.saw_socket import SaWSocket
from lib.options import DownloadOptions, UploadOptions
from lib.file_handler.file_sender.client_file_sender import ClientFileSender
from lib.file_handler.file_receiver.client_file_receiver import (
    ClientFileReceiver,
)
from lib.operation_codes import OperationCodes


def print_upload_usage():
    print(
        "usage: upload [-h] [-v | -q] [-H ADDR] [-p PORT] [-s FILEPATH] [-n FILENAME]",
        end="\n\n",
    )
    print(
        "A file will be uploaded to the server. The default file name if not specified will be grabbed from the enviroment variable. If there is an existent file with the same name, it will be named <file_name>(n).",
        end="\n\n",
    )
    print("optional arguments:")
    print("-h, --help show this help message and exit")
    print("-v, --verbose increase output verbosity")
    print("-q, --quiet decrease output verbosity")
    print("-H, --host service IP address")
    print("-p, --port service port")
    print("-s, --storage storage dir path")


def print_download_usage():
    print(
        "usage: download [-h] [-v | -q] [-H ADDR] [-p PORT] [-d FILEPATH] [-n FILENAME]",
        end="\n\n",
    )
    print(
        "A file will be downloaded from the server. The default file name if not specified will be grabbed from the enviroment variable. If there is an existent file with the same name at the selected path, it will be overwritten.",
        end="\n\n",
    )
    print("optional arguments:")
    print("-h, --help show this help message and exit")
    print("-v, --verbose increase output verbosity")
    print("-q, --quiet decrease output verbosity")
    print("-H, --host server IP address")
    print("-p, --port server port")
    print("-d, --dst destination file path")
    print("-n, --name file name")


class Client:
    @classmethod
    def upload(cls):
        options = UploadOptions(sys.argv[1:])
        if options.show_help:
            print_upload_usage()
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
        if options.show_help:
            print_download_usage()
            return
        logger = Logger("client", options.verbose, options.quiet)
        server_address = (options.host, options.port)
        ClientFileReceiver(
            options.file_name,
            dest_path=options.dst,
            logger=logger,
            opposite_address=server_address,
        ).handle_receive_process()
