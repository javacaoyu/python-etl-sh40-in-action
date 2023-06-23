# coding:utf8
"""
barcode的service
"""

from day02.util.mysql_util import *
from day02.config.db_config import *
from day02.util.logger_util import *
from day02.util.time_util import *
from day02.config.project_config import *
from day02.model.barcode_model import *


class BarcodeService:
    def __init__(self):
        self.target_mysql_util = MySQLUtil(
            host=target_host,
            port=target_port,
            user=target_user,
            passwd=target_passwd,
            charset=target_charset
        )
        self.metadata_mysql_util = MySQLUtil(
            host=metadata_host,
            port=metadata_port,
            user=metadata_user,
            passwd=metadata_passwd,
            charset=metadata_charset
        )
        self.source_mysql_util = MySQLUtil(
            host=source_host,
            port=source_port,
            user=source_user,
            passwd=source_passwd,
            charset=source_charset
        )
        self.logger = logger_util.get_logger()

        self.max_update_time = None     # 记录本次操作的最大时间用于存储元数据
        self.barcode_csv_path = csv_output_root_path + \
            "/barcode_" + get_time("%Y-%m-%d_%H_%M_%S") + "csv.tmp"

    def start(self):
        # 1.查询元数据库获得上一次的时间
        last_update = self.get_last_update()
        # 2.组装sql语句 查询数据源表
        res = self.query_source_data(last_update)
        # 3.封装查询结果到模型
        models_list = self.get_models_list(res)
        # 4.写出MYSQL和CSV
        self.__write(models_list)
        # 5.记录元数据

    def get_last_update(self):
        sql = f"insert into {metadata_barcode_processed_table_name} values(" \
              f"null,'{self.max_update_time}',{get_time()})"

        self.metadata_mysql_util.conn.autocommit(False) # 关闭自动提交
        self.metadata_mysql_util.conn.begin()           # 开启事务

        try:
            self.metadata_mysql_util.execute(metadata_db_name,sql)
        except Exception as e:
            self.logger.critical(f"[mysql数据采集]元数据记录失败，请立即检查，SQL：{sql}")
            self.metadata_mysql_util.conn.rollback()        # 事务回滚
            raise e
        self.metadata_mysql_util.conn.commit()              # 事务提交


    def __write(self,models_list:list):
        """
        将数据写入带mysql和csv
        :param models_list: 数据列表
        :return: None
        """
        self.target_mysql_util.conn.autocommit(False)       # 关闭自动提交
        self.target_mysql_util.conn.begin()                 # 开启事务
        try:
            self.__write_to_mysql(models_list)
            self.__write_tocsv(models_list)
        except Exception as e:
            self.target_mysql_util.conn.rollback()          # 出错误回滚
            self.logger.error(f"[mysql数据采集]写出数据到MySQL或CSV出错，回滚，程序退出。")
            raise e
        self.target_mysql_util.conn.commit()                # 提交

        # csv改名


    def get_models_list(self, query_result):
        models_list = []
        for line_tuple in query_result:
            model = BarcodeModel(line_tuple)
            models_list.append(model)
        return models_list

    def query_source_data(self, last_update):
        """
        读取源表的数据
        :param last_update: 上次读取的时间
        :return: 查询到的结果
        """
        sql = None
        if last_update:
            sql = f"select * from {source_barcode_table_name} " \
                  f"where updateAt >= '{last_update}' order by updateAt"
        else:
            # 第一次的时候，last_update为NONE
            sql = f"select * from {source_barcode_table_name} " \
                  f"order by updateAt"
        result = self.source_mysql_util.query(
            db=source_db_name,
            sql=sql
        )

        return result


