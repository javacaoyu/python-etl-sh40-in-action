# coding:utf8
"""
订单业务模型
"""


from config import project_config, db_config
from util.str_util import substr


class LogsModel:

    def __init__(self, data_str: str, sep="\t"):
        arrs = data_str.split(sep)

        self.log_time = arrs[0]  # 日志时间
        self.log_level = arrs[1].replace("[", "").replace("]", "")  # 日志级别,处理方括号
        self.log_module = arrs[2]  # 日志模块
        self.response_time = int(arrs[3][:-2][5:])  # 响应时间提取
        self.province = arrs[4]  # 省份
        self.city = arrs[5]  # 城市
        self.log_text = arrs[6]                                     # 日志正文

    def generate_insert_sql(self, table_name=db_config.target_logs_table_name):
        sql = f"INSERT INTO {table_name}(" \
              f"log_time, log_level, log_module, response_time, province, city, log_text) VALUES(" \
              f"'{substr(self.log_time,0,19)}', " \
              f"'{self.log_level}', " \
              f"'{self.log_module}', " \
              f"{self.response_time}, " \
              f"'{self.province}', " \
              f"'{self.city}', " \
              f"'{self.log_text}'" \
              f")"
        return sql

    def to_csv(self):
        csv_line= \
            f"{self.log_time}{project_config.csv_output_sep}" \
            f"{self.log_level}{project_config.csv_output_sep}" \
            f"{self.log_module}{project_config.csv_output_sep}" \
            f"{self.response_time}{project_config.csv_output_sep}" \
            f"{self.province}{project_config.csv_output_sep}" \
            f"{self.city}{project_config.csv_output_sep}" \
            f"{self.log_text}{project_config.csv_output_sep}"
        return csv_line



    @staticmethod
    def get_csv_header():
        logs_header_str = \
            f"log_time{project_config.csv_output_sep}" \
            f"log_level{project_config.csv_output_sep}" \
            f"log_module{project_config.csv_output_sep}" \
            f"response_time{project_config.csv_output_sep}" \
            f"province{project_config.csv_output_sep}" \
            f"city{project_config.csv_output_sep}" \
            f"log_text"
        return logs_header_str
