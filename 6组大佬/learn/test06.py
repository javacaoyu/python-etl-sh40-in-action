import time

# strftime -> str formate time 得到指定格式的时间字符串
# 将时间转化为字符串
res = time.strftime("%Y-%m-%d", time.localtime())
print(res)

# 时间戳转换  时间戳：距离1970-01-01 00:00:00多少秒
# 将时间戳转化为时间字符串
res = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(1686872236))
print(res)
