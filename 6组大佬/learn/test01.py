import pymysql
from pymysql import Connection

conn: Connection = pymysql.Connect(
    host='127.0.0.1',
    user='root',
    password='123456',
    port=3306,
    charset='utf8'
)
# 打印数据库版本信息
print(conn.get_server_info())

# 如果执行SQL，需要获得cursor对象
cursor = conn.cursor()
# 执行创建数据库
cursor.execute("CREATE DATABASE if not exists TEST_SH40 CHARSET UTF8")
# 选择数据库
conn.select_db("TEST_SH40")
# 创建表
cursor.execute("CREATE TABLE test(id int, name varchar(255))")

# 关闭连接
conn.close()
