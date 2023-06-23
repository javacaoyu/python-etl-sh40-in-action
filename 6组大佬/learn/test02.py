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
cursor.execute("INSERT INTO test values(1, 'zxl')")
cursor.execute("INSERT INTO test values(2, 'aaa')")
cursor.execute("INSERT INTO test values(3, 'bbb')")
# 需要提交事务
conn.commit()


# 关闭连接
conn.close()
