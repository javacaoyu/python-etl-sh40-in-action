# coding:utf8
"""
logs数据采集，启动逻辑
"""
from service.logs_service import LogsDataService
if __name__ == '__main__':
    LogsDataService().start()


"""
从逻辑封装中，LogsDataService类是对：
- 从logs读取文件
- 判断元数据找出需要处理的文件
- 转换成模型
- 转换为sql插入mysql
- 转换为csv字符串写入文件
这一系列操作，都可以被LogsDataService类所包含，我们只需要获得
LogsDataService类的一个实例对象，点击start启动即可。
"""