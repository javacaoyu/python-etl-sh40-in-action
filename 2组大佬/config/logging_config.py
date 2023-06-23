# coding:utf8
"""
记录日志相关配置
"""
import os
from day02.util import time_util
# 日志输出的根目录在当前python项目根目录内的logs文件夹内，全部写入到这个文件夹
default_logger_file_root_path = f"{os.path.dirname(os.getcwd())}/logs/"

# 日志文件名，按天，一天一个日志文件
default_logger_file_basename = f"pyetl_{time_util.get_today()}.log"

# 设置日志默认级别：普通
default_logger_level = 20
# 日志的绝对路径
default_logger_file_full_path = default_logger_file_root_path+default_logger_file_basename
# 设置日志默认输出到文件的格式
default_logger_formatter = "%(asctime)s - [%(levelname)s] - %(filename)s[line:%(lineno)d]: %(message)s"
