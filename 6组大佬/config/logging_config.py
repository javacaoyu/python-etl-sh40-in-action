"""
记录日志相关配置项
"""
import os
from util import time_util
# os.getcwd()  # 当前所在路径
# os.path.dirname() # 获取当前文件夹的父文件夹

# 日志输出的根目录在当前python项目根目录内的logs文件夹中，全部都写入到这个文件夹下
# default_logger_file_root_path = f"{os.path.dirname(os.getcwd())}/logs/"
default_logger_file_root_path = "F:/study/PycharmProjects/ETL/day01/logs/"

# 日志的文件名  天
default_logger_file_basename = f"pyetl_{time_util.get_today()}.log"
# 日志文件完整路径
default_logger_file_full_path = f"{default_logger_file_root_path}{default_logger_file_basename}"
# 默认日志级别20（info）
default_logger_level = 20
# 默认日志格式
default_logger_formatter = "%(asctime)s - [%(levelname)s] - %(filename)s[line:%(lineno)d]: %(message)s"
