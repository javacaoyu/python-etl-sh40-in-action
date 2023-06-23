from config import project_config, db_config
# - 日志时间
# - 日志级别
# - 日志模块
# - 相应时间毫秒数
# - 省份
# - 城市
# - 日志信息
#
# > 列的分隔符是：`\t`


class LogModel:
    def __init__(self, list1):
        """
        请按照以下顺序将list传入
        # - 日志时间 logs_time
        # - 日志级别 logs_level
        # - 日志模块 logs_module
        # - 相应时间毫秒数 response_time
        # - 省份 province
        # - 城市 city
        # - 日志信息 logs_info
        #
        :param list1:
        """
        self.logs_time = list1[0]
        self.logs_level = list1[1]
        self.logs_module = list1[2]
        self.response_time = list1[3]
        self.province = list1[4]
        self.city = list1[5]
        self.logs_info = list1[6]

    def generate_insert_sql(self, table_name=db_config.target_logs_table_name):
        sql = f"insert into {table_name} values (" \
              f"null," \
              f"\'{self.logs_time.split('.')[0]}\'," \
              f"\'{self.logs_level.replace('[','').replace(']','')}\'," \
              f"'{self.logs_module}'," \
              f"\'{self.response_time.split(':')[1].replace('ms','')}\'," \
              f"'{self.province}'," \
              f"'{self.city}'," \
              f"'{self.logs_info}'" \
              f")"
        return sql

    def to_csv(self, sep=project_config.log_csv_ouput_sep):
        line_csv = f"{self.logs_time}{sep}" \
                   f"{self.logs_level}{sep}" \
                   f"{self.logs_module}{sep}" \
                   f"{self.response_time}{sep}" \
                   f"{self.province}{sep}" \
                   f"{self.city}{sep}" \
                   f"{self.logs_info}" \
                   f""
        return line_csv


    @staticmethod
    def to_csv_header(sep=project_config.log_csv_ouput_sep):
        line_header = f"logs_time{sep}" \
                      f"logs_level{sep}" \
                      f"logs_module{sep}" \
                      f"response_time{sep}" \
                      f"province{sep}" \
                      f"city{sep}" \
                      f"logs_inf"
        return line_header
