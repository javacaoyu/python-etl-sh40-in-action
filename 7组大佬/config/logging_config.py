# coding:utf8
"""
记录日志相关的配置项
"""
import os
from util.str_util import unite_path_slash
from util.time_util import get_today

# 日志输出的根目录在当前Python项目根目录内的logs文件夹中，全部都写入到这个文件夹
default_logger_file_root_path = "D:\PycharmProjects\standardisation\logs\\"
# 日志的文件名，按天来，一天一个日志文件
default_logger_file_basename = f"orders_{get_today('%Y%m%d')}.log"
backend_data_default_logger_file_basename = f"backend_data_{get_today('%Y%m%d')}.log"

default_logger_level = 20  # 默认日志级别
default_logger_file_full_path = \
    unite_path_slash(f"{default_logger_file_root_path}"
                     f"{default_logger_file_basename}")  # 默认日志输出位置
backend_data_default_logger_file_full_path = \
    unite_path_slash(f"{default_logger_file_root_path}"
                     f"{backend_data_default_logger_file_basename}")  # 默认日志输出位置
default_logger_formatter = \
    "%(asctime)s - [%(levelname)s] - %(filename)s[line:%(lineno)d]: %(message)s"
