import logging

# 1获得一个Logger对象
logger: logging.Logger = logging.getLogger("sh40_logger")

# 2给logger设置一些特殊属性
# 2.1 指定logger输出日志文件位置
file_handle = logging.FileHandler("E:\\sh40.log", 'a', encoding='utf8')
# 2.2 指定logger输出日志内容格式
fmt = logging.Formatter("%(asctime)s - [%(levelname)s] - %(filename)s[line:%(lineno)d]: %(message)s")

# 3 使输出格式生效。需要将格式提供给handler
file_handle.setFormatter(fmt)
# 3 使输出位置生效。需要将handler给logger对象
logger.addHandler(file_handle)


