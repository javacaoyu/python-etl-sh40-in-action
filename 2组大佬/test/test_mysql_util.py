# coding:utf
"""
mysql工具类的单元测试
切记！切记！切记！
- 单元测试连接数据库一般单独找一个数据库实例或者单独创建一个库用
- 单元测试千万不要连接生产（正式应用）数据库实例
"""
from unittest import TestCase
from day02.util.mysql_util import *
from day02.config.db_config import *


class TestMySQLUtil(TestCase):
    def setUp(self) -> None:
        """
        执行任何测试方法前，先跑这个方法
        :return:
        """
        # print("我先执行")
        self.sqlModel = MySQLUtil(
            host=unittest_host,
            port=unittest_port,
            user=unittest_user,
            passwd=unittest_passwd,
            charset=unittest_charset
        )
        self.sqlModel.conn.select_db(unittest_db_name)

    def test_query(self):
        # print("我是测试方法")
        self.sqlModel.execute(unittest_db_name, 'drop table if exists test_query')

        # 创建新表
        self.sqlModel.execute(unittest_db_name, 'create table test_query(id int,name varchar(10))')
        # 插入测试数据
        self.sqlModel.execute_force_commit(unittest_db_name, "insert into test_query values(1,'周杰伦')")
        r = self.sqlModel.query(unittest_db_name, "select * from test_query")
        excepted = ((1, '周杰伦'),)
        self.assertEqual(excepted, r)

    def test_check_table_exists(self):
        # 准备环境一致,假设查询的表是:test_exists
        self.sqlModel.execute(unittest_db_name, 'drop table if exists test_query')

        # 当前表不存在
        r = self.sqlModel.check_table_exists(unittest_db_name, 'test_exists')
        self.assertFalse(r)

        # 创建新表
        self.sqlModel.execute(unittest_db_name, 'create table test_exists(id int)')
        r = self.sqlModel.check_table_exists(unittest_db_name, 'test_exists')
        self.assertTrue(r)

    def test_check_and_create_table(self):
        # 准备环境一致,假设判断表:test_exists_and_create
        self.sqlModel.execute(unittest_db_name, 'drop table if exists test_exists_and_create')

        # 表不存在,创建,返回True
        r = self.sqlModel.check_and_create_table(unittest_db_name, 'test_exists_and_create', 'id int')
        self.assertTrue(r)
        r = self.sqlModel.check_table_exists(unittest_db_name, 'test_exists_and_create')
        self.assertTrue(r)

        # 表存在,结果为False
        r = self.sqlModel.check_and_create_table(unittest_db_name, 'test_exists_and_create', 'id int')
        self.assertFalse(r)

    def test_execute(self):
        # 准备测试环境,表:test_execute
        self.sqlModel.execute(unittest_db_name, 'drop table if exists test_execute')

        # 创建
        self.sqlModel.check_and_create_table(unittest_db_name, 'test_execute', 'id int,name varchar(10)')
        # 执行insert,自动提交为False
        self.sqlModel.conn.autocommit(False)
        self.sqlModel.execute(unittest_db_name, "insert into test_execute values(1,'周杰伦')")

        # 为验证结果正确,应当断开重连,避免连接对象的缓存查到缓存的未提交的数据
        self.sqlModel.conn.close()
        self.sqlModel.conn.connect()

        r = self.sqlModel.query(unittest_db_name, 'select * from test_execute')
        self.assertEqual(len(r), 0)

        # 执行insert,自动提交为True
        self.sqlModel.conn.autocommit(True)
        self.sqlModel.execute(unittest_db_name, "insert into test_execute values(1, '周杰伦')")

        self.sqlModel.conn.close()
        self.sqlModel.conn.connect()

        r = self.sqlModel.query(unittest_db_name, 'select * from test_execute')
        self.assertEqual(((1, '周杰伦'), ), r)

    def test_execute_force_commit(self):
        # 准备测试环境,表:test_execute_force_commit
        self.sqlModel.execute(unittest_db_name, 'drop table if exists test_execute_force_commit')

        # 创建
        self.sqlModel.check_and_create_table(unittest_db_name, 'test_execute_force_commit', 'id int,name varchar(10)')

        # 执行insert,自动提交为False
        self.sqlModel.conn.autocommit(False)
        self.sqlModel.execute_force_commit(unittest_db_name, "insert into test_execute_force_commit values(1,'周杰伦')")

        # 为了验证结果正确,断开连接
        self.sqlModel.conn.close()
        self.sqlModel.conn.connect()

        r = self.sqlModel.query(unittest_db_name, 'select * from test_execute_force_commit')
        self.assertEqual(((1, '周杰伦'),), r)

    def tearDown(self) -> None:
        """
        任何测试方法结束后，执行
        :return:
        """
        print("执行结束,清理表")
        self.sqlModel.execute(unittest_db_name, 'drop table if exists test_query')
        self.sqlModel.execute(unittest_db_name, 'drop table if exists test_exists')
        self.sqlModel.execute(unittest_db_name, 'drop table if exists test_exists_and_create')
        self.sqlModel.execute(unittest_db_name, 'drop table if exists test_execute')
        self.sqlModel.execute(unittest_db_name, 'drop table if exists test_execute_force_commit')

        self.sqlModel.close()
