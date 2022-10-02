import os

class ExecutionOptions:
    DEFAULT_HOST = "127.0.0.1"
    DEFAULT_SERVER_PORT = 8000

    def __init__(self, arguments):
        self.arguments = arguments
        self.parse_options()

    def parse_options(self):
        self.show_help = "-h" in self.arguments or "--help" in self.arguments
        self.verbose = "-v" in self.arguments or "--verbose" in self.arguments
        self.quiet = "-q" in self.arguments or "--quiet" in self.arguments
        host_index = (
            self.arguments.index("-H")
            if "-H" in self.arguments
            else self.arguments.index("--host")
            if "--host" in self.arguments
            else -1
        )
        self.host = (
            self.arguments[host_index + 1] if host_index > -1 else self.DEFAULT_HOST
        )
        port_index = (
            self.arguments.index("-p")
            if "-p" in self.arguments
            else self.arguments.index("--port")
            if "--port" in self.arguments
            else -1
        )
        self.port = (
            self.arguments[port_index + 1]
            if port_index > -1
            else self.DEFAULT_SERVER_PORT
        )


class ClientOptions(ExecutionOptions):
    DEFAULT_FILE_NAME = "untitled"

    def __init__(self, arguments):
        super().__init__(arguments)

    def parse_options(self):
        super().parse_options()
        self.file_name_index = (
            self.arguments.index("-n")
            if "-n" in self.arguments
            else self.arguments.index("--name")
            if "--name" in self.arguments
            else -1
        )
        self.file_name = (
            self.arguments[self.file_name_index + 1]
            if self.file_name_index > -1
            else self.DEFAULT_FILE_NAME
        )


class UploadOptions(ClientOptions):
    DEFAULT_SRC_PATH = ""

    def __init__(self, arguments):
        super().__init__(arguments)

    def parse_options(self):
        super().parse_options()
        self.src_index = (
            self.arguments.index("-s")
            if "-s" in self.arguments
            else self.arguments.index("--src")
            if "--src" in self.arguments
            else -1
        )
        self.src = (
            self.arguments[self.src_index + 1]
            if self.src_index > -1
            else self.DEFAULT_SRC_PATH
        )

    def valid(self):
        return type(self.port) == int and os.path.isfile(self.src)

class DownloadOptions(ClientOptions):
    DEFAULT_DEST_FOLDER = "files/downloaded"

    def __init__(self, arguments):
        super().__init__(arguments)

    def parse_options(self):
        super().parse_options()
        self.dst_index = (
            self.arguments.index("-d")
            if "-d" in self.arguments
            else self.arguments.index("--dst")
            if "--dst" in self.arguments
            else -1
        )
        self.dst = (
            self.arguments[self.dst_index + 1]
            if self.dst_index > -1
            else self.DEFAULT_DEST_FOLDER
        )
    
    def valid(self):
        return type(self.port) == int and os.path.isdir(self.dst)


class ServerOptions(ExecutionOptions):
    DEFAULT_STORAGE = "files/uploaded"

    def __init__(self, arguments):
        super().__init__(arguments)

    def parse_options(self):
        super().parse_options()
        self.storage_index = (
            self.arguments.index("-s")
            if "-s" in self.arguments
            else self.arguments.index("--storage")
            if "--storage" in self.arguments
            else -1
        )
        self.storage = (
            self.arguments[self.storage_index + 1]
            if self.storage_index > -1
            else self.DEFAULT_STORAGE
        )
    def valid(self):
        return type(self.port) == int and os.path.isdir(self.storage)
