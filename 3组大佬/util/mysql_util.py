import pymysql
from util import logging_util


class MySQLutil:
    def __init__(self, host, port, user, password):
        self.conn = pymysql.Connection(
            host=host,
            port=port,
            user=user,
            password=password,
            charset="UTF8"
        )
        self.logger = logging_util.get_logger()


    def close_autocommit(self):
        self.conn.autocommit(False)

    def query(self, db, sql):
        """
        提供sql查询的结果
        :param db: 数据库
        :param sql: 查询语句
        :return: 查询结果，返回元组套元组
        """
        cursor = self.conn.cursor()
        self.conn.select_db(db)
        cursor.execute(sql)
        r = cursor.fetchall()
        cursor.close()
        return r

    def query_result_list(self, db, sql):
        """
        讲query方法的查询结果转化为list
        :param db: 数据库
        :param sql: 查询语句
        :return: 查询结果，返回list套元组
        """
        r = self.query(db, sql)
        result_list = []
        for i in r:
            result_list.append(i)
        return result_list

    def query_result_single_column(self, db, sql):
        list1 = self.query_result_list(db, sql)
        r_list = []
        for i in list1:
            r_list.append(i[0])
        return r_list

    def check_table_exists(self, db, table_name):
        """
        查询指定表是否存在
        :param db: 数据库
        :param table_name:指定表名
        :return: 存在返回True，不存在返回False
        """
        r = self.query_result_list(db, 'show tables')
        for i in r:
            if table_name in i[0]:
                return True
        return False

    def check_table_and_create(self, db, table_name, cols_define):
        """
        检查指定表是否存在，不存在则创建
        :param db: 数据库名
        :param table_name: 指定表名
        :param cols_define: 表结构，列定义
        :return: False 表已存在，True 表创建成功
        """
        if self.check_table_exists(db, table_name):
            self.logger.warning(f"表{table_name}已存在，本方法不创建，跳过。")
            return False
        sql = f"create table {table_name}({cols_define})"
        self.execute(db, sql)
        return True

    def close(self):
        self.conn.close()

    def execute(self, db, sql):
        """
        执行对sql的操作，包括创建和插入
        :param db: 数据库
        :param sql: sql语句
        :return: none
        """
        self.conn.select_db(db)
        cursor = self.conn.cursor()
        try:
            cursor.execute(sql)
        except Exception as e:
            self.logger.warning(f"执行sql语句错误，语句为：{sql}")
            raise e

    def execute_commit(self, db, sql):
        """
        对execute执行语句并提交
        :param db: 数据库
        :param sql: 执行语句
        :return: none
        """
        self.execute(db, sql)
        self.conn.commit()
