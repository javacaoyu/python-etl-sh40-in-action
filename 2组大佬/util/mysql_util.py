# coding:utf8
"""
MySQL工具类
- 构建链接
- 数据查询
- 数据插入
- 检查表是否存在
- 创建表
"""
import pymysql
from day02.util import logger_util


class MySQLUtil:
    def __init__(self, host, port, user, passwd, charset):
        self.conn = pymysql.Connect(
            host=host,
            port=port,
            user=user,
            password=passwd,
            charset=charset
        )
        self.logger = logger_util.get_logger()

    def query(self, db, sql):
        """
        数据库查询
        :param db: 数据库
        :param sql: sql
        :return: 查询结果
        """
        cursor = self.conn.cursor()
        self.conn.select_db(db)
        cursor.execute(sql)
        res = cursor.fetchall()
        cursor.close()
        return res

    def query_result_list(self, db, sql):
        """
        以列表形式返回查询结果
        :param db:
        :param sql:
        :return:
        """
        r = self.query(db, sql)
        r_list = []
        for t in r:
            r_list.append(t)
        return r_list

    def check_table_exists(self, db, table_name):
        """
        检查表是否存在
        :param db: 数据库
        :param table_name: 表名
        :return: True表存在，False表不存在
        """
        r = self.query_result_list(db, "show tables")
        if (table_name,) in r:
            return True
        return False

    def check_and_create_table(self, db, table_name, cols_define):
        """
        检查表，不存在创建
        :param cols_define: 字段
        :param db: 数据库
        :param table_name: 表名
        :return: True创建成功，False创建失败
        """
        if not self.check_table_exists(db, table_name):
            self.conn.select_db(db)
            sql = f"create table {table_name}({cols_define})"
            self.execute(db, sql)
            self.logger.info(f"执行了sql建表语句，{sql}")
            return True
        else:
            self.logger.warning(f"表：{table_name}已经存在,本方法不创建，跳过")
            return False

    def execute(self, db, sql) -> None:
        """
        执行无返回值的相关的sql语句，如create,insert等
        不关心是否自动提交
        :param db: 数据库
        :param sql: 执行语句
        :return: None
        """
        self.conn.select_db(db)
        cursor = self.conn.cursor()
        try:
            cursor.execute(sql)
        except Exception as e:
            self.logger.error(f"执行sql语句出错，执行的sql是：{sql}")
            raise e

    def execute_force_commit(self, db, sql) -> None:
        """
        执行无返回值的相关的sql语句，如create,insert等
        手动提交
        :param db: 数据库
        :param sql: 执行语句
        :return: None
        """
        self.execute(db, sql)
        self.conn.commit()

    def query_result_single_column(self, db, sql):
        """
        针对单列的select查询,将结果封装到list内返回
        提示:如果你查询到多列,结果也只返回第一列
        :param db: 数据库
        :param sql: sql语句
        :return: list
        """
        r = self.query(db, sql)
        r_list = []
        for line_tuple in r:
            r_list.append(line_tuple[0])
        return r_list

    def close(self):
        self.conn.close()
