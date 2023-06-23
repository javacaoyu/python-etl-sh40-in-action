# coding:utf8
"""
日志输出相关的工具代码文件
"""

import logging
from config import logging_config


# 设置返回日志
def get_logger(
        log_path=logging_config.default_logger_file_full_path,
        level=logging_config.default_logger_level,
        formatter=logging_config.default_logger_formatter
):
    logger = logging.getLogger()
    # if len(logger.handlers) > 0:
    #     return logger
    logger.handlers = []
    logger.setLevel(level)
    file_handler = logging.FileHandler(log_path, 'a', encoding='utf8')
    fmt = logging.Formatter(formatter)
    file_handler.setFormatter(fmt)
    logger.addHandler(file_handler)
    return logger
