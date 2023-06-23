import os.path
import sys

import my_logging
import my_handler

logger = my_logging.MyLogger()
logger.setLevel(my_logging.DEBUG)

file_handler = my_handler.MyFileHandler("E:/test_log.log", 'a', encoding='utf8')
stream_handler = my_handler.MyStreamHandler()

fmt = my_logging.MyFormatter(fmt=3)

file_handler.setFormatter(fmt)
stream_handler.setFormatter(fmt)

logger.addHandler(file_handler)
logger.addHandler(stream_handler)

logger.debug("啦啦啦")
logger.info("哒哒哒")
logger.warning("锵锵锵")
logger.error("咚咚咚")
logger.critical("铛铛铛")

print(os.path.basename(sys.argv[0]))  # logger_test.py
print(sys._getframe().f_lineno)  # 28
"%(asctime)s - [%(levelname)s] - %(filename)s[line:%(lineno)d]: %(message)s"
