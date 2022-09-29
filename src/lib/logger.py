import logging
from colorlog import ColoredFormatter


class Logger(object):

    def __init__(self, name, is_verbose, is_quiet):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(self.define_log_level(is_verbose, is_quiet))
        message_format = "  %(log_color)s%(levelname)-8s%(reset)s | %(log_color)s%(message)s%(reset)s"
        formatter = ColoredFormatter(message_format)
        self.ch = logging.StreamHandler()
        # self.ch.setLevel(logging.DEBUG)
        self.ch.setFormatter(formatter)
        self.logger.addHandler(self.ch)

    def define_log_level(self, is_verbose, is_quiet):
        if is_verbose:
            return logging.DEBUG
        if is_quiet:
            return logging.ERROR
        return logging.WARNING

    def debug(self, msg):
        self.logger.debug(msg)

    def info(self, msg):
        self.logger.info(msg)

    def warning(self, msg):
        self.logger.warning(msg)

    def error(self, msg):
        self.logger.error(msg)

    def critical(self, msg):
        self.logger.critical(msg)
