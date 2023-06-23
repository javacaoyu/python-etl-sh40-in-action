import pymysql

conn: pymysql.Connection = pymysql.connect(
    host='127.0.0.1',
    user='root',
    password='123456',
    port=3306,
    charset='utf8'
)

cursor = conn.cursor()

cursor.execute("create database if not exists test_sh40 charset utf8")
conn.select_db("test_sh40")
# cursor.execute("create table if not exists test1(num int, name varchar(255))")
# for i in range(1, 101):
#     cursor.execute(f"insert into test1 values({i},'a')")
# conn.commit()
cursor.execute("select * from test1")
res = cursor.fetchall()
names = []
for item in res:
    names.append(item[0])
print(names)

conn.close()

