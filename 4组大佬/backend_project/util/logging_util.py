# coding:utf8
"""
日志输出相关的工具代码文件
"""
import logging
from config import logging_config

def get_logger(log_path=logging_config.default_logger_file_full_path,
               level=logging_config.default_logger_level,
               formatter=logging_config.default_logger_formatter):
    """
    返回一个设置好的logger对象
    :param log_path: 日志输出路径
    :param level: 日志输出级别
    :param formatter: 日志输出格式
    :return: logging.Logger对象
    """
    # 构建logger对象
    logger = logging.getLogger('python-etl')

    # 设置级别
    logger.setLevel(level)

    # 创建FileHandler对象
    file_handler = logging.FileHandler(filename=log_path,mode='a',encoding='UTF-8')

    # 创建Formatter对象
    fmt = logging.Formatter(fmt=formatter)

    # 向Handler对象设置fmt显示格式
    file_handler.setFormatter(fmt)

    # 向logger对象设置Handler4
    logger.addHandler(file_handler)

    # 返回logger对象
    return logger

