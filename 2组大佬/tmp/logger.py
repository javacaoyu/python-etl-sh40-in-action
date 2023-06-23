# coding:utf8
"""
logging模块演示
"""
import logging

#1.获得一个类对象，这个类是Logger类，可以通过logging模块的getLogger方法获取
logger:logging.Logger=logging.getLogger("sh40_logger")

#2.logger正常可以直接使用，直接logger.info("信息")可以直接输出，但是没有其他信息，格式也不好
#给logger设置一些特殊的属性，比如：
# - 指定logger输出的日志文件位置
# - 指定logger输出的日志内容格式

#指定位置通过Handler对象来决定，所以，先构建一个Handler对象
file_handler=logging.FileHandler("e:\\sh40.log",'a','UTF-8')
#日志的格式通过Fotmatter对象决定，先构建一个Formatter对象
fmt=logging.Formatter("%(asctime)s - [%(levelname)s] - %(filename)s[line:%(lineno)d]: %(message)s")

#3.让输出位置和输出格式生效
#让格式生效，需要将格式提供给handler
file_handler.setFormatter(fmt)

#让输出位置生效，将handler给logger对象
logger.addHandler(file_handler)


#logger对象可用
logger.warning("测试警告")
logger.error("测试错误")
