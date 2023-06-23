import time

import my_handler

CRITICAL = 50
ERROR = 40
WARNING = 30
INFO = 20
DEBUG = 10
NOTSET = 0


class MyFormatter(object):
    def __init__(self, fmt):
        self.formatter_str = fmt

class MyLogger(object):
    def __init__(self):
        self.level = 0
        self.handler = []
        self.file = None
        self.now = ""
        self.status = "NOTSET"

    def setLevel(self, level):
        self.level = level

    # CRITICAL = 50
    # ERROR = 40
    # WARNING = 30
    # INFO = 20
    # DEBUG = 10
    # NOTSET = 0
    def debug(self, msg):
        if self.level <= 10:
            self.status = "debug"
            for item in self.handler:
                item.output(msg, self.status)

    def info(self, msg):
        if self.level <= 20:
            self.status = "info"
            for item in self.handler:
                item.output(msg, self.status)

    def warning(self, msg):
        if self.level <= 30:
            self.status = "warning"
            for item in self.handler:
                item.output(msg, self.status)

    def error(self, msg):
        if self.level <= 40:
            self.status = "error"
            for item in self.handler:
                item.output(msg, self.status)

    def critical(self, msg):
        if self.level <= 50:
            self.status = "critical"
            for item in self.handler:
                item.output(msg, self.status)

    def addHandler(self, handler: my_handler.MyFileHandler):
        self.handler.append(handler)




