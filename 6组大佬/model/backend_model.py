"""
日志模型
"""
from config import db_config, project_config


class BackendModel(object):
    def __init__(self, data: str):
        """
        可以传入日志字符串，元素顺序为：
        - backend_time  日志产生时间
        - backend_type  日志类型
        - file_name  文件名
        - response_time  响应时间
        - province  省份
        - city  城市
        - backend_info  日志信息
        :param data: 日志字符串
        """
        data = data.split('\t')
        self.backend_time = data[0][0:19]
        self.backend_type = data[1][1:-1]
        self.file_name = data[2]
        self.response_time = data[3].split(':')[1]
        self.province = data[4]
        self.city = data[5]
        self.backend_info = data[6].replace(',', '，')

    def generate_insert_sql(self, table_name=db_config.target_backend_table_name) -> str:
        """
        生成插入sql语句
        :param table_name: 要插入的数据表名
        :return:
        """
        sql = f"INSERT IGNORE INTO {table_name}(" \
              f"id,backend_time,backend_type,file_name,response_time," \
              f"province,city,backend_info) values (" \
              f"NULL," \
              f"'{self.backend_time}'," \
              f"'{self.backend_type}'," \
              f"'{self.file_name}'," \
              f"'{self.response_time}'," \
              f"'{self.province}'," \
              f"'{self.city}'," \
              f"'{self.backend_info}')"

        return sql

    def to_csv(self, sep=project_config.csv_output_sep) -> str:
        """
        生成csv信息行
        :param sep: 分割符
        :return:
        """
        csv_line = f"{self.backend_time}{sep}" \
                   f"{self.backend_type}{sep}" \
                   f"{self.file_name}{sep}" \
                   f"{self.response_time}{sep}" \
                   f"{self.province}{sep}" \
                   f"{self.city}{sep}" \
                   f"{self.backend_info}"

        return csv_line

    @staticmethod
    def get_csv_header(sep=project_config.csv_output_sep) -> str:
        """
        生成csv标头
        :param sep: 分隔符
        :return:
        """
        csv_head_line = f"backend_time{sep}" \
                        f"backend_type{sep}" \
                        f"file_name{sep}" \
                        f"response_time{sep}" \
                        f"province{sep}" \
                        f"city{sep}" \
                        f"backend_info"

        return csv_head_line
