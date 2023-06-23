# coding:utf8
"""
MySQL数据库工具类
可以提供：
- 构建链接
- 数据查询
- 数据插入
- 检查表是否存在
- 创建表
"""
import pymysql
from util import logging_util


class MysqlUtil:
    def __init__(self, host, port, user, password, charset='utf8'):
        self.conn = pymysql.Connect(
            host=host,
            port=port,
            user=user,
            password=password,
            charset=charset
        )
        self.logger = logging_util.get_logger()

    def query(self, db, sql):
        """
        提供SQL查询的结果
        :param db:待查询数据库
        :param sql:查询语句
        :return:
        """
        cursor = self.conn.cursor()
        self.conn.select_db(db)
        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close()
        return result

    def query_result_list(self, db, sql):
        result = self.query(db, sql)
        result_list = []
        for r in result:
            result_list.append(r)
        return result_list

    def query_result_single_column(self, db, sql):
        """
        针对单列的SELECT查询，将结果封装到list内返回
        Note：如果你查询了多列，结果也只返回第一列
        :param db: 数据库
        :param sql: 查询SQL
        :return: list
        """
        r = self.query(db, sql)
        r_list = []  # 结果list
        for line_tuple in r:
            r_list.append(line_tuple[0])

        return r_list

    def check_table_exists(self, db, table_name):
        """
        检查指定的表是否存在
        :param db: 数据库
        :param table_name: 表名
        :return: True 存在，False 不存在
        """
        result = self.query_result_list(db, 'show tables')
        if (table_name,) in result:
            return True
        return False

    def check_and_create_table(self, db, table_name, cols_define):
        """
        检查表，如果不存在，就创建它
        :param db: 数据库
        :param table_name: 被创建的表名
        :param cols_define: 列定义，比如 id int, name varchar(255)
        :return: True 创建成功， False 表已经存在或创建失败
        """
        if not self.check_table_exists(db, table_name):
            cursor = self.conn.cursor()
            cursor.execute(f"create table {table_name}({cols_define})")
            cursor.close()
            return True
        else:
            self.logger.warning(f"表{table_name}已存在，创建失败！")
            return False

    def close(self):
        self.conn.close()

    def execute(self, db, sql):
        """
        执行无返回值的相关sql语句，如create、insert等
        不关系是否自动提交
        :param db: 操作的数据库
        :param sql: 执行的sql
        :return: None
        """
        cursor = self.conn.cursor()
        self.conn.select_db(db)
        try:
            cursor.execute(sql)
        except Exception as e:
            self.logger.error(f"执行sql语句：{sql}出错！")
            raise e  # 仍然让程序报错停止，在报错前执行error语句

    def execute_force_commit(self, db, sql):
        """
        执行无返回值的相关sql语句，如create、insert等
        100%提交
        :param db: 操作的数据库
        :param sql: 执行的sql
        :return: None
        """
        self.execute(db, sql)
        self.conn.commit()

    def disable_autocommit(self):
        """
        关闭自动提交
        :return: None
        """
        self.conn.autocommit(False)
