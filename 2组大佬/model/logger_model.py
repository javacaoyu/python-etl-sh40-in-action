# coding:utf8
"""
读取日志文件的模型

"""
from day02.config.db_config import *
from day02.config.project_config import *
from day02.util.str_util import *

class LoggerModel:
    """ 2023-06-23 10:01:12.778191	[INFO]	event.py	响应时间:786ms	江苏省	南京市	学IT来黑马，就来黑马程序员 """
    def __init__(self,log_str:str):
        log_list = log_str.split('\t')
        self.logger_time = log_list[0]
        self.level = log_list[1]
        self.file = log_list[2]
        self.response_time = log_list[3]
        self.province = log_list[4]
        self.city = log_list[5]
        self.comment = log_list[6]

    def generate_insert_sql(self,table_name=target_logger_table_name):
        """
        组装sql插入语句
        :param table_name:
        :return:
        """
        # str_util工具的函数clean_str添加去除[]，已测试
        # time_util工具添加函数str_to_time函数，去除毫秒，已测试
        # str_util工具添加函数clean_respone，对于响应时间只取数字，已测试
        sql = f"insert into {table_name}(" \
              f"id,logger_time,level,file,respone_time,province,city,comment)" \
              f"values(" \
              f"null," \
              f"'{str_to_time(self.logger_time)}'," \
              f"'{clean_str(self.level)}'," \
              f"'{self.file}'," \
              f"{clean_respone(self.response_time)}," \
              f"'{self.province}'," \
              f"'{self.city}'," \
              f"'{self.comment}'" \
              f")"
        return sql

    def to_csv(self,sep=csv_output_sep):
        """
        组装csv文件的写入格式
        :param sep:
        :return:
        """
        csv_line = f"{str_to_time(self.logger_time)}{sep}" \
                   f"{clean_str(self.level)}{sep}" \
                   f"{self.file}{sep}" \
                   f"{clean_respone(self.response_time)}{sep}" \
                   f"{self.province}{sep}" \
                   f"{self.city}{sep}" \
                   f"{self.comment}"
        return csv_line


    @staticmethod
    def get_csv_header(sep=csv_output_sep):
        """
        组装csv文件的头
        :param sep:
        :return:
        """
        csv_header = f"logger_time{sep}" \
                     f"level{sep}" \
                     f"file{sep}" \
                     f"response_time{sep}" \
                     f"province{sep}" \
                     f"city{sep}" \
                     f"comment"
        return csv_header


