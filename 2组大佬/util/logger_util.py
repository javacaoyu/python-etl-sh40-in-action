# coding:utf8
"""
日志相关的工具包
"""
import logging
from day02.config import logging_config


def get_logger(
        log_path=logging_config.default_logger_file_full_path,
        level=logging_config.default_logger_level,
        formatter=logging_config.default_logger_formatter):
    """
    返回一个配置好的logger对象
    :param log_path: 日志输出的文件路径，提供默认值
    :param level: 日志输出级别，默认info：20
    :param formatter: 日志输出格式，默认
    :return: logging.logger对象
    """
    # 构建logger对象
    logger: logging.Logger = logging.Logger("python-etl")

    # 设置级别
    logger.setLevel(level)

    # 创建FileHandler对象
    file_handler = logging.FileHandler(
        filename=log_path,  # 日志输出文件路径
        mode='a',  # 日志文件打开模式，追加
        encoding='UTF-8'
    )

    # 创建Formatter对象
    fmt = logging.Formatter(formatter)

    # 让格式生效，将格式给handler
    file_handler.setFormatter(fmt)

    # 让输出路径和格式生效，将handler给logger
    logger.addHandler(file_handler)

    # 返回配置好的logger对象
    return logger
