# coding:utf8
"""
订单业务模型
"""

from config import project_config, db_config
from datetime import datetime
from util import str_util
from util import time_util

class LogsDataModel:
    def __init__(self,data_str: str):
        """
        传入字符串（即log文件的行），将每列数据抽取出来封装进列表。
        :param data_str: log文件行
        """
        data_list = data_str.split("\t")            # 分隔符'\t'

        string = data_list[0]

        # 将字符串转换为datetime对象
        dt = datetime.strptime(string, "%Y-%m-%d %H:%M:%S.%f")

        # 去除微秒
        dt_without_us = dt.replace(microsecond=0)

        # 将datetime对象转换回字符串
        formatted_string = dt_without_us.strftime("%Y-%m-%d %H:%M:%S")

        self.data_ts = formatted_string             # 日志时间,去除毫秒
        self.log_level = data_list[1].strip("[]")   # 日志级别
        self.log_module = data_list[2]              # 日志模块
        self.response_time = data_list[3].split(':')[-1]           # 响应时间毫秒数
        self.province = data_list[4]                # 省份
        self.city = data_list[5]                    # 城市
        self.log_msg = data_list[6]                 # 日志信息

    def get_insert_sql(self,table_name=db_config.target_logs_data_table_name):
        """
        生成插入SQL语句
        :param table_name: 要插入的目标表名
        :return: 插入数据的SQL语句
        """
        sql = f"insert ignore into {table_name}(" \
              f"data_ts,log_level,log_module,response_time," \
              f"province,city,log_msg) values(" \
              f"{str_util.check_null_transform_to_str(self.data_ts)}," \
              f"{str_util.check_null_transform_to_str(self.log_level)}," \
              f"{str_util.check_null_transform_to_str(self.log_module)}," \
              f"{str_util.check_null_transform_to_str(self.response_time)}," \
              f"{str_util.check_null_transform_to_str(self.province)}," \
              f"{str_util.check_null_transform_to_str(self.city)}," \
              f"{str_util.check_null_transform_to_str(self.log_msg)})"
        return sql

    def to_csv(self):
        csv_line = f"{self.data_ts}{project_config.csv_output_sep}" \
                   f"{self.log_level}{project_config.csv_output_sep}" \
                   f"{self.log_module}{project_config.csv_output_sep}" \
                   f"{self.response_time}{project_config.csv_output_sep}" \
                   f"{self.province}{project_config.csv_output_sep}" \
                   f"{self.city}{project_config.csv_output_sep}" \
                   f"{self.log_msg}{project_config.csv_output_sep}"
        return csv_line

    @staticmethod
    def get_csv_header():
        logs_header_str = f"dataTS{project_config.csv_output_sep}" \
                          f"logLevel{project_config.csv_output_sep}" \
                          f"logModule{project_config.csv_output_sep}" \
                          f"responseTime{project_config.csv_output_sep}" \
                          f"province{project_config.csv_output_sep}" \
                          f"city{project_config.csv_output_sep}" \
                          f"logMsg{project_config.csv_output_sep}"
        return logs_header_str

