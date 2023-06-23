# coding:utf-8
"""
记录日志相关的配置项
"""
import os
from untils import time_util

# 日志输出的根目录在当前Python项目根目录内的logs文件夹中，全部都写入到这个文件夹
log_root_path = f"{os.path.dirname(os.getcwd())}/project_ETL/logs/"
# 日志的文件名，按天来，一天一个日志文件
log_file_name = f"pyetl_{time_util.get_today()}.log"

# 日志等级
"""
DEBUG: 10
INFO: 20
WARNING: 30
ERROR: 40
CRITICAL: 50
"""
logger_level = 20

# 日志器名称
log_logger_name = "python-etl"

# 默认日志输出位置
log_file_path = f"{log_root_path}{log_file_name}"

# 日志格式
log_fomatter = "%(asctime)s - [%(levelname)s] - %(filename)s[line:%(lineno)d]: %(message)s"
