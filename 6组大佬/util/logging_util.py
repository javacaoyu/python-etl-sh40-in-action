"""
日志输出相关
"""
import logging
from config import logging_config


def get_logger(log_path=logging_config.default_logger_file_full_path,
               level=logging_config.default_logger_level,
               formatter=logging_config.default_logger_formatter) -> logging.Logger:
    """
    返回一个设置好的logger对象
    :param log_path: 日志输出文件路径
    :param level: 日志输出级别，默认info 20
    :param formatter: 日志显示格式
    :return:
    """
    logger = logging.getLogger("python-etl")

    if len(logger.handlers) > 0:
        return logger

    logger.setLevel(level)

    # 输出到文件
    file_handler = logging.FileHandler(
        filename=log_path,
        mode='a',
        encoding='utf8'
    )
    # 输出到控制台
    stream_handler = logging.StreamHandler()

    # 日志格式
    fmt = logging.Formatter(fmt=formatter)

    # 添加设定的日志格式
    file_handler.setFormatter(fmt)
    stream_handler.setFormatter(fmt)

    # 添加handler
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

    return logger
