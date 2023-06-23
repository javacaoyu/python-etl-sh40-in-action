import os
import sys
import time
import my_logging
from typing import IO


class MyHandler(object):
    def __init__(self):
        self.formatter = None
        self.now = ""

    def setFormatter(self, fmt):
        self.formatter = fmt

    def output(self, msg, status):
        pass

class MyFileHandler(MyHandler):
    def __init__(self, filename, mode, encoding):
        super().__init__()
        self.filename = filename
        self.mode = mode
        self.encoding = encoding
        self.file = open(
            file=self.filename,
            mode=self.mode,
            encoding=self.encoding)

    def output(self, msg, status):
        if self.formatter.formatter_str == 3:
            self.now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        if self.formatter.formatter_str == 2:
            self.now = time.strftime("%Y-%m-%d")
        self.file.write(f"{self.now} {status} {os.path.basename(sys.argv[0])} {sys._getframe().f_lineno} {msg}")
        self.file.write("\n")


class MyStreamHandler(MyHandler):
    def __init__(self):
        super().__init__()

    def output(self, msg, status):
        if self.formatter.formatter_str == 3:
            self.now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        if self.formatter.formatter_str == 2:
            self.now = time.strftime("%Y-%m-%d")
        if status == "debug":
            print(f"\033[38m{self.now} {status} {os.path.basename(sys.argv[0])} {sys._getframe().f_lineno} {msg}\033[0m")
        if status == "info":
            print(f"\033[38m{self.now} {status} {os.path.basename(sys.argv[0])} {sys._getframe().f_lineno} {msg}\033[0m")
        if status == "warning":
            print(f"\033[33m{self.now} {status} {os.path.basename(sys.argv[0])} {sys._getframe().f_lineno} {msg}\033[0m")
        if status == "error":
            print(f"\033[31m{self.now} {status} {os.path.basename(sys.argv[0])} {sys._getframe().f_lineno} {msg}\033[0m")
        if status == "critical":
            print(f"\033[31m{self.now} {status} {os.path.basename(sys.argv[0])} {sys._getframe().f_lineno} {msg}\033[0m")


