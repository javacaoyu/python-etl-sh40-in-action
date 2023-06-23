from util.mysql_util import MySQLutil
from config import db_config


class BarcodeService:
    def __init__(self):
        self.target_mysql_util = MySQLutil(
            host=db_config.target_host,
            port=db_config.target_port,
            user=db_config.target_user,
            password=db_config.target_password
        )

    def start(self):
        # 需要处理的文件
        # 转model对象
        # 写出mysql和csv文件
        # 写入元数据
        pass
