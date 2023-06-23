import os
import shutil

# 判断是否文件
print(os.path.isfile("E:\\tlias.py"))
print(os.path.isfile("F:\\study"))

# 判断是否文件夹
print(os.path.isdir("E:\\tlias.py"))
print(os.path.isdir("F:\\study"))

# 创建文件夹
os.makedirs()

# 判断路径是否存在
os.path.exists()

# 删除文件
os.remove()

# 删除文件夹  等同于rm -rf
shutil.rmtree()
