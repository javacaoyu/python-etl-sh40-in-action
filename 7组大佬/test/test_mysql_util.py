from unittest import TestCase
from config import db_config
from util import mysql_util


class TestMysqlUtil(TestCase):
    def setUp(self) -> None:
        """
        在任何测试方法之前执行此函数
        :return:
        """
        self.test_mysql = mysql_util.MysqlUtil(
            host=db_config.unittest_host,
            port=db_config.unittest_port,
            user=db_config.unittest_user,
            password=db_config.unittest_password,
            charset=db_config.unittest_charset
        )
        self.test_mysql.conn.select_db(db_config.unittest_db_name)

    def test_query(self):
        # 准备环境一致，假设查询的表是：test_query
        self.test_mysql.execute(db_config.unittest_db_name, 'drop table if exists test_query')
        # 创建新表
        self.test_mysql.execute(db_config.unittest_db_name, 'create table test_query(id int, name varchar(255))')
        # 插入数据
        self.test_mysql.execute_force_commit(db_config.unittest_db_name, 'insert into test_query values(1,"张三")')
        self.assertEqual(((1, "张三"),), self.test_mysql.query(db_config.unittest_db_name, 'select * from test_query'))

    def test_check_table_exists(self):
        # 准备环境
        self.test_mysql.execute(db_config.unittest_db_name, 'drop table if exists test_exists')
        self.assertFalse(self.test_mysql.check_table_exists(db_config.unittest_db_name, 'test_exists'))
        self.test_mysql.execute(db_config.unittest_db_name, 'create table test_exists(id int, name varchar(255))')
        self.assertTrue(self.test_mysql.check_table_exists(db_config.unittest_db_name, 'test_exists'))

    def test_check_and_create_table(self):
        # 准备环境
        self.test_mysql.execute(db_config.unittest_db_name, 'drop table if exists test_exists_create')
        self.assertTrue(self.test_mysql.check_and_create_table(
            db_config.unittest_db_name,
            'test_exists_create',
            'id int, name varchar(255)'
        )
        )
        # 再次检测是否存在
        self.assertTrue(self.test_mysql.check_table_exists(db_config.unittest_db_name, 'test_exists_create'))
        self.assertFalse(self.test_mysql.check_and_create_table(
            db_config.unittest_db_name,
            'test_exists_create',
            'id int, name varchar(255)'
        )
        )

    def test_execute(self):
        # 准备环境一致，假设查询的表是：test_execute
        self.test_mysql.execute(db_config.unittest_db_name, 'drop table if exists test_execute')
        # 创建新表
        self.test_mysql.execute(db_config.unittest_db_name, 'create table test_execute(id int, name varchar(255))')
        self.test_mysql.conn.autocommit(False)  # 关闭自动提交
        self.test_mysql.execute(db_config.unittest_db_name, 'insert into test_execute values(1, "张三")')
        # 为了验证结果正确，应当断开链接重连，避免从链接对象的缓存（缓冲区）查到缓存的未提交的数据
        self.test_mysql.conn.close()  # 断开，清空缓存如果缓存内有数据自动提交是True就提交，是False就丢弃
        self.test_mysql.conn.connect()  # 重新连接
        self.assertEqual(0, len(self.test_mysql.query(db_config.unittest_db_name, 'select * from test_execute')))

        # 执行insert语句且自动提交
        self.test_mysql.conn.autocommit(True)
        self.test_mysql.execute(db_config.unittest_db_name, 'insert into test_execute values(1, "张三")')
        # 断开连接
        self.test_mysql.conn.close()
        self.test_mysql.conn.connect()
        self.assertEqual(((1, "张三"),),
                         self.test_mysql.query(db_config.unittest_db_name, 'select * from test_execute'))

    def test_execute_force_commit(self):
        # 准备环境
        self.test_mysql.execute(db_config.unittest_db_name, 'drop table if exists test_execute_commit')
        self.test_mysql.execute(db_config.unittest_db_name,
                                'create table test_execute_commit(id int, name varchar(255))')
        self.test_mysql.conn.autocommit(False)  # 关闭自动提交
        self.test_mysql.execute_force_commit(db_config.unittest_db_name,
                                             'insert into test_execute_commit values(1, "张三")')
        self.test_mysql.conn.close()
        self.test_mysql.conn.connect()
        self.assertEqual(((1, "张三"),),
                         self.test_mysql.query(db_config.unittest_db_name, 'select * from test_execute_commit'))

    def tearDown(self) -> None:
        """
        在所有方法执行之后执行此函数
        :return:
        """
        # 清理测试库
        self.test_mysql.execute(db_config.unittest_db_name, 'drop table if exists test_query')
        self.test_mysql.execute(db_config.unittest_db_name, 'drop table if exists test_exists')
        self.test_mysql.execute(db_config.unittest_db_name, 'drop table if exists test_exists_create')
        self.test_mysql.execute(db_config.unittest_db_name, 'drop table if exists test_execute')
        self.test_mysql.execute(db_config.unittest_db_name, 'drop table if exists test_execute_commit')
        self.test_mysql.close()
