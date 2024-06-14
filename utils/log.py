import datetime
import logging
import os

DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


class Logger:
    """logger instance 생성을 위한 클래스"""

    def __init__(self, file):
        """logger를 하나 생성함. handler의 경우 중복 방지"""
        self.logger = logging.getLogger("MyLogger")
        self.file_name = file

        if len(self.logger.handlers) == 0:
            # StreamHandler
            formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
            stream_handler = logging.StreamHandler()
            stream_handler.setFormatter(formatter)

            self.logger.addHandler(stream_handler)
            self.logger.setLevel(logging.INFO)

    def info(self, value):
        """logger의 info level"""
        self.logger.info(f"{str(value)} (at {self.file_name})")

    def warning(self, value):
        """logger의 warning level"""
        self.logger.warning(f"{str(value)} (at {self.file_name})")

    def error(self, value):
        """logger의 error level"""
        self.logger.error(f"{str(value)} (at {self.file_name})")


def datetime_now():
    """현재 시간을 return"""
    return datetime.datetime.now().strftime(DATE_FORMAT)
