import logging

from config import logging_config


def get_logger(log_path=logging_config.log_file_path):
    log_logger_name = logging_config.log_logger_name
    log_level = logging_config.logger_level
    log_fomatter = logging_config.log_fomatter

    # 1. 想要使用logging模块对外输出日志，需要先获得Logger对象
    logger = logging.getLogger(log_logger_name)

    # 2. 设置日志级别
    """
    DEBUG: 10
    INFO: 20
    WARNING: 30
    ERROR: 40
    CRITICAL: 50
    """
    logger.setLevel(log_level)

    # 3. 显示日志的输出格式，构建Formatter类对象
    fmt = logging.Formatter(log_fomatter)

    # 4. 创建Handler（handler决定了日志输出的位置，比如控制台或文件）， 如果输出文件，应该得到FileHandler对象
    file_handler = logging.FileHandler(
        # f"./logs/{get_time('%Y%m%d_%H%M%S')}.log",      # 输出日志文件的位置
        log_path,  # 输出日志文件的位置
        mode='a',  # 模式，a，追加
        encoding='utf-8'  # 编码 utf-8
    )

    # 5. 将日志输出格式，赋予handler对象
    file_handler.setFormatter(fmt)

    # 6. 将handler对象，赋予logger对象。
    logger.addHandler(file_handler)

    # 7. 目前的logger对象就可以用了
    # formatter格式，设置给了file_handler对象
    # file_handler是设置的写文件，赋予了logger对象
    # logger.error("error哈哈哈哈哈哈")
    # logger.info("info哈哈哈哈哈哈")
    # logger.debug("debug哈哈哈哈哈哈")
    return logger
