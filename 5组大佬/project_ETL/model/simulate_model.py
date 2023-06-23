import re

from config import simulate_log_config as slc


class Simulate:
    def __init__(self, data):
        """
        模拟数据模型
        :param data: 2023-06-23 10:07:18.842562	[INFO]	goods_manager.py	响应时间:85ms	山东省	青岛市	看啥呢，别看日志了，快写代码，说的就是你。
        """
        data_list = data.split("\t")  # 切割数据
        self.date = data_list[0].strip()
        self.level = data_list[1].strip()[1:-1]
        self.file = data_list[2].strip()
        self.time = re.match(r".*:(\d+)ms", data_list[3]).group(1)
        self.province = data_list[4].strip()
        self.region = data_list[5].strip()
        self.data = data_list[6].strip()

    def generate_insert_sql(self, table_name=slc.simulate_table_name):
        """生成INSERT SQL语句"""
        sql = f"""
        INSERT IGNORE INTO {table_name}(
            date,
            level,
            file,
            time,
            province,
            region,
            data
        )
        VALUE (
            '{self.date}',
            '{self.level}',
            '{self.file}',
            '{self.time}',
            '{self.province}',
            '{self.region}',
            '{self.data}'
        )
        """
        return sql
