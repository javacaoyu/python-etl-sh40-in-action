import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

file_handler = logging.FileHandler("E:/test.log", 'a', encoding='utf8')
stream_handler = logging.StreamHandler()

fmt = logging.Formatter("%(asctime)s %(levelname)s %(filename)s %(lineno)d %(message)s")

file_handler.setFormatter(fmt)
stream_handler.setFormatter(fmt)

logger.addHandler(file_handler)
logger.addHandler(stream_handler)

logger.info("啦啦啦")
logger.info("哒哒哒")


"""
附录:Formatter参数列表
%(name)s            日志对象名称 (logging channel)
%(levelno)s         日志级别对应的数字 (DEBUG, INFO,
                    WARNING, ERROR, CRITICAL)
%(levelname)s       日志级别字符串 ("DEBUG", "INFO",
                    "WARNING", "ERROR", "CRITICAL")
%(pathname)s        全路径 (if available)
%(filename)s        调用输出日志的Python代码文件名称
%(module)s          Python代码文件所在的模块 (name portion of filename)
%(lineno)d          输出日志的行号
                    (if available)
%(funcName)s        输出日志代码所在的方法名称
%(created)f         日志时间（非格式化） (time.time()
                    return value)
%(asctime)s         格式化日志时间
%(msecs)d           Millisecond portion of the creation time
%(relativeCreated)d Time in milliseconds when the LogRecord was created,
                    relative to the time the logging module was loaded
                    (typically at application startup time)
%(thread)d          Thread ID (if available)
%(threadName)s      Thread name (if available)
%(process)d         Process ID (if available)
%(message)s         日志信息本是
"""



