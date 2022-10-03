from threading import Thread
from time import time

from src.lib.file_handler.file_sender.file_sender import FileSender


class ServerFileSender(FileSender, Thread):
    def __init__(self, file_data, source_dir, **kwargs):
        super().__init__(**kwargs)
        port, file_size, file_name = self.socket.deserialize_information(file_data)
        self.file_name = file_name
        self.source_dir = source_dir
        Thread.__init__(self)

    def run(self):
        start_time = time()
        self.handle_process_start()
        if self.file_size == -1:
            self.logger.error(f"File {self.file_name} not found")
            self.socket.close_connection()
            return
        file_sent_success = self.send_file(
            file_path=f"{self.source_dir}/{self.file_name}"
        )
        self.socket.close_connection()
        finish_time = time()
        self.log_final_send_status(file_sent_success, finish_time - start_time)

    def _handle_send_process(self):
        # just for polymorphism purposes
        self.start()

    def handle_process_start(self):
        self.file_size = self.get_file_size(f"{self.source_dir}/{self.file_name}")
        self.socket.send_sv_information(file_size=self.file_size)
