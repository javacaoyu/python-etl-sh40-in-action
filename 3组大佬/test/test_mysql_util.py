# coding = utf-8

from unittest import TestCase

import pymysql

from config import db_config
from util.mysql_util import MySQLutil


class TestMysqlUtil(TestCase):
    def setUp(self) -> None:
        '''执行任何测试方法前，先执行内容'''
        self.mysql_util = MySQLutil(
            host=db_config.unittest_host,
            port = db_config.unittest_port,
            user=db_config.unittest_user,
            password=db_config.unittest_password
        )
        self.mysql_util.conn.select_db(db_config.unittest_db_name)

    def test_query_result_list(self):
        # 准备环境一致，假设查询的表是：test_query
        self.mysql_util.execute(db_config.unittest_db_name,"drop table if exists test_query")
        # # 创建新表
        self.mysql_util.check_table_and_create(db_config.unittest_db_name,"test_query","id int,name varchar(255)")
        # self.mysql_util.execute(db_config.unittest_db_name, 'create table test_query(id int, name varchar(10))')
        # # 插入测试数据
        self.mysql_util.execute_commit(db_config.unittest_db_name,"insert into test_query values(1,'周杰伦')")
        r = self.mysql_util.query_result_list(db_config.unittest_db_name,"select * from test_query")
        excepted = [(1,'周杰伦')]
        self.assertEqual(excepted,r)

    def test_check_table_exists(self):
        # 准备环境，测试表：test_exists
        self.mysql_util.execute(db_config.unittest_db_name,"drop table if exists test_exists")
        # 调用check_table_exists,判断是否存在，存在返回true，不存在返回False
        r = self.mysql_util.check_table_exists(db_config.unittest_db_name, "test_exists")
        self.assertFalse(r)
        # 创建test_exists，再次判断
        self.mysql_util.execute(db_config.unittest_db_name,"create table test_exists(id int)")
        r = self.mysql_util.check_table_exists(db_config.unittest_db_name, "test_exists")
        self.assertTrue(r)

    def test_check_and_create_table(self):
        # 准备环境一致，假设判断的表是：test_exists_and_create
        self.mysql_util.execute(db_config.unittest_db_name, 'drop table if exists test_exists_and_create')

        # 表不存在，要走创建，返回值应该是True
        r = self.mysql_util.check_table_and_create(db_config.unittest_db_name, 'test_exists_and_create', 'id int')
        self.assertTrue(r)
        r = self.mysql_util.check_table_exists(db_config.unittest_db_name, 'test_exists_and_create')  # 再次检查是否存在
        self.assertTrue(r)

        # 表存在，结果应当是False
        r = self.mysql_util.check_table_and_create(db_config.unittest_db_name, 'test_exists_and_create', 'id int')
        self.assertFalse(r)

    def test_execute(self):
        # 准备测试环境, 表：test_execute
        self.mysql_util.execute(db_config.unittest_db_name, 'drop table if exists test_execute')  # 先删除
        # 再创建
        self.mysql_util.check_table_and_create(db_config.unittest_db_name, 'test_execute', 'id int, name varchar(10)')
        # 执行insert，自动提交为False
        self.mysql_util.conn.autocommit(False)
        self.mysql_util.execute(db_config.unittest_db_name, "insert into test_execute values(1, '周杰轮')")
        # 为了验证结果正确，应当断开链接重连，避免从链接对象的缓存（缓冲区）查到缓存的未提交的数据
        self.mysql_util.conn.close()  # 断开，清空缓存如果缓存内有数据自动提交是True就提交，是False就丢弃
        self.mysql_util.conn.connect()  # 连接

        r = self.mysql_util.query(db_config.unittest_db_name, 'select * from test_execute')
        self.assertEqual(len(r), 0)

        # 执行insert，自动提交为True
        self.mysql_util.conn.autocommit(True)
        self.mysql_util.execute(db_config.unittest_db_name, "insert into test_execute values(1, '周杰轮')")
        # 为了验证结果正确，应当断开链接重连
        self.mysql_util.conn.close()  # 断开
        self.mysql_util.conn.connect()  # 连接

        r = self.mysql_util.query(db_config.unittest_db_name, 'select * from test_execute')
        self.assertEqual(((1, '周杰轮'),), r)

    def test_execute_force_commit(self):
        # 准备测试环境, 表：test_execute_force_commit
        self.mysql_util.execute(db_config.unittest_db_name, 'drop table if exists test_execute_force_commit')  # 先删除
        # 再创建
        self.mysql_util.check_table_and_create(db_config.unittest_db_name, 'test_execute_force_commit',
                                               'id int, name varchar(10)')
        # 执行insert，自动提交为False
        self.mysql_util.conn.autocommit(False)  # 主动设置为False，验证是否能100%提交
        self.mysql_util.execute_commit(db_config.unittest_db_name,
                                             "insert into test_execute_force_commit values(1, '周杰轮')")

        # 为了验证结果正确，应当断开链接重连
        self.mysql_util.conn.close()  # 断开
        self.mysql_util.conn.connect()  # 连接

        r = self.mysql_util.query(db_config.unittest_db_name, 'select * from test_execute_force_commit')
        self.assertEqual(((1, '周杰轮'),), r)

    def tearDown(self) -> None:
        '''执行完成任何方法后，执行内容'''
        self.mysql_util.execute(db_config.unittest_db_name,"drop table if exists test_query")
        self.mysql_util.execute(db_config.unittest_db_name,"drop table if exists test_exists")
        self.mysql_util.execute(db_config.unittest_db_name, 'drop table if exists test_exists_and_create')
        self.mysql_util.execute(db_config.unittest_db_name, 'drop table if exists test_execute')
        self.mysql_util.execute(db_config.unittest_db_name, 'drop table if exists test_execute_force_commit')
        print('我完成测试后执行')