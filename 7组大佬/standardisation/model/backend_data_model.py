from util import str_util
from config import db_config, project_config


class BackendDataModel:
    def __init__(self, data):
        """
        传入数据按照以下顺序：
        - 日志时间
        - 日志级别
        - 日志模块
        - 响应时间毫秒数
        - 省份
        - 城市
        - 日志信息
        :param data:
        """
        data = str_util.replace_comma(data).split("\t")
        self.date_time = str_util.remove_millisecond(data[0])
        self.level = str_util.remove_fist_last(data[1])
        self.mode = data[2]
        self.response_time = str_util.fetch_number(data[3])
        self.province = data[4]
        self.city = data[5]
        self.note = data[6]

    def generate_insert_sql(self, table_name=db_config.target_backend_data_table_name):
        sql = f"insert into {table_name}(" \
              f"id,date_time,level,mode,response_time,province,city,note) values(" \
              f"null," \
              f"'{self.date_time}'," \
              f"'{self.level}'," \
              f"'{self.mode}'," \
              f"{self.response_time}," \
              f"'{self.province}'," \
              f"'{self.city}'," \
              f"'{self.note}'" \
              f")"
        return sql

    @staticmethod
    def get_csv_header():
        csv_header_str = f"dataTime{project_config.csv_output_sep}" \
                         f"level{project_config.csv_output_sep}" \
                         f"mode{project_config.csv_output_sep}" \
                         f"response_time{project_config.csv_output_sep}" \
                         f"province{project_config.csv_output_sep}" \
                         f"city{project_config.csv_output_sep}" \
                         f"note"
        return csv_header_str

    def to_csv(self):
        csv_line = f"{self.date_time}{project_config.csv_output_sep}" \
                   f"{self.level}{project_config.csv_output_sep}" \
                   f"{self.mode}{project_config.csv_output_sep}" \
                   f"{self.response_time}{project_config.csv_output_sep}" \
                   f"{self.province}{project_config.csv_output_sep}" \
                   f"{self.city}{project_config.csv_output_sep}" \
                   f"{self.note}"
        return csv_line
