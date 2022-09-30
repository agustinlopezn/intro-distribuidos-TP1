from threading import Thread
import time

CYCLE_TIME = 1


class ThreadCleaner(Thread):
    def __init__(self, active_threads, logger):
        super().__init__()
        self.active_threads = active_threads
        self.logger = logger

    def run(self):
        while True:
            self.clean_threads()
            time.sleep(CYCLE_TIME)

    def clean_threads(self):
        addresses_to_delete = [
            key for key, thread in self.active_threads.items() if not thread.is_alive()
        ]
        for client_address in addresses_to_delete:
            thread = self.active_threads[client_address]
            thread.join()
            del self.active_threads[client_address]
            self.logger.debug(f"Thread listening to {client_address} deleted")
