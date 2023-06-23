"""
条码数据采集核心业务逻辑代码
"""
from util import mysql_util
from config import db_config

class BarcodeService:
    def __init__(self):
        self.metadata_mysql_util= mysql_util.MySQLUtil(
            host=db_config.metadata_host,
            port=db_config.metadata_port,
            user=db_config.metadata_user,
            password=db_config.metadata_password,
            charset=db_config.metadata_charset
        )
        self.source_mysql_util = mysql_util.MySQLUtil(
            host=db_config.metadata_host,
            port=db_config.metadata_port,
            user=db_config.metadata_user,
            password=db_config.metadata_password,
            charset=db_config.metadata_charset
        )
        self.target_mysql_util = mysql_util.MySQLUtil(
            host=db_config.metadata_host,
            port=db_config.metadata_port,
            user=db_config.metadata_user,
            password=db_config.metadata_password,
            charset=db_config.metadata_charset
        )

    def start(self):
        # todo 1获取需要处理的数据
        # todo 2转model对象
        # todo 3写出MySQL和csv
        # todo 4记录元数据
        # todo 5结束
        pass