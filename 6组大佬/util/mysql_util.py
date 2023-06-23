"""
mysql数据库工具类
提供：
- 构建连接
- 数据查询
- 数据插入
- 检查表是否存在
- 创建表
"""
import pymysql
from util import logging_util


class MySQLUtil:
    def __init__(self, host, port, user, password, charset='utf8'):
        self.conn = pymysql.Connect(
            host=host,
            port=port,
            user=user,
            password=password,
            charset=charset
        )
        self.logger = logging_util.get_logger()

    def disable_autocommit(self):
        self.conn.autocommit(False)
    def query(self, db, sql):
        """
        提供sql查询结果
        :param db: 要查询的数据库
        :param sql: 要查询的sql语句
        :return: 双层嵌套元组
        """
        self.conn.select_db(db)
        cursor = self.conn.cursor()
        cursor.execute(sql)
        res = cursor.fetchall()
        cursor.close()
        return res

    def query_result_list(self, db, sql):
        """
        提供sql查询结果
        :param db: 要查询的数据库
        :param sql: 要查询的sql语句
        :return: 列表内嵌元组
        """
        res_list = []
        res = self.query(db, sql)
        for item in res:
            res_list.append(item)
        return res_list

    def check_table_exists(self, db, table_name) -> bool:
        """
        检查数据库中是否存在某表
        :param db: 要查询的数字库
        :param table_name: 要查询的表的名字
        :return: bool 存在True  不存在False
        """
        pass
        res = self.query_result_list(db, "show tables")
        if (table_name,) in res:
            return True
        return False

    def check_and_create_table(self, db, table_name, cols_define) -> bool:
        """
        检查表，如果不存在就创建
        :param db: 要查询的数字库
        :param table_name: 要查询的表的名字
        :return: 创建 True  已存在False
        """
        if self.check_table_exists(db, table_name):
            self.logger.warning(f"表{table_name}已存在，不可重复建表")
            return False
        self.conn.select_db(db)
        self.execute(db, f"CREATE TABLE {table_name} ({cols_define})")
        return True

    def close(self) -> None:
        """
        断开与MySQL的连接
        :return:
        """
        self.conn.close()

    def execute(self, db, sql):
        """
        执行无返回值的SQL语句，如create, insert
        Note：不关心是否提交
        :param db: 操作的数据库
        :param sql: 执行的sql
        :return: None
        """
        self.conn.select_db(db)
        cursor = self.conn.cursor()
        try:
            cursor.execute(sql)
        except Exception as e:
            self.logger.error(f"执行SQL出错，执行的SQL语句是{sql}")
            raise e

    def execute_force_commit(self, db, sql) -> None:
        """
        执行无返回值的SQL语句，如create, insert
        Note: 100%提交
        :param db: 操作的数据库
        :param sql: 执行的sql
        :return: None
        """
        self.execute(db, sql)
        self.conn.commit()

    def query_result_single_column(self, db, sql):
        """
        针对单列的SELECT查询，将结果封装到list内返回
        :param db: 数据库
        :param sql: 查询sql
        :return: list
        """
        r = self.query(db, sql)
        r_list = []
        for line_tuple in r:
            r_list.append(line_tuple[0])
        return r_list

