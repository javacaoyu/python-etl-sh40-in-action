import pymysql
from pymysql import Connection

conn: Connection = pymysql.Connect(
    host='127.0.0.1',
    user='root',
    password='123456',
    port=3306,
    charset='utf8',
    autocommit=False
)
# 打印数据库版本信息
print(conn.get_server_info())

# 如果执行SQL，需要获得cursor对象
cursor = conn.cursor()
conn.select_db("test_sh40")
cursor.execute("select * from test")
res = cursor.fetchall()
print(res)  # ((1, 'zxl'), (2, 'aaa'), (3, 'bbb'))


# 关闭连接
conn.close()
