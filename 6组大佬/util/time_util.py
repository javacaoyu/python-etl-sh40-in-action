"""
时间工具
"""
import time

# 10位是秒级
def second_ts_to_date_str(ts, formatter="%Y-%m-%d %H:%M:%S") -> str:
    """
    秒级时间戳转日期字符串
    :param ts:
    :param formatter:
    :return:
    """
    return time.strftime(formatter, time.localtime(ts))


# 13位是毫秒级
def millisecond_ts_to_date_str(ts, formatter="%Y-%m-%d %H:%M:%S") -> str:
    """
    秒级时间戳转日期字符串
    :param ts:
    :param formatter:
    :return:
    """
    return time.strftime(formatter, time.localtime(ts/1000))


def get_time(formatter="%Y-%m-%d %H:%M:%S") -> str:
    """
    获取当前时间
    :param formatter: 时间格式
    :return: 时间字符串
    """
    return time.strftime(formatter, time.localtime())


def get_today(formatter="%Y-%m-%d") -> str:
    """
    获取当前时间
    :param formatter: 时间格式
    :return: 时间字符串
    """
    return get_time(formatter=formatter)
