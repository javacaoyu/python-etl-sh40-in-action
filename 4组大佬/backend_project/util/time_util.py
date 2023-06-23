import time

def second_ts_to_datetime(ts,timeformat='%Y-%m-%d %H:%M:%S') -> str:
    """
    秒单位时间戳转换成指定格式时间，默认年-月-日 时:分:秒
    :param ts: 被转换时间戳
    :param timeformat: 期望被转换成的时间格式
    :return: 时间格式字符串
    """
    return time.strftime(timeformat,time.localtime(ts))

def millisecond_ts_to_datetime(ts,timeformat='%Y-%m-%d %H:%M:%S') -> str:
    """
    秒单位时间戳转换成指定格式时间，默认年-月-日 时:分:秒
    :param ts: 被转换时间戳
    :param timeformat: 期望被转换成的时间格式
    :return: 时间格式字符串
    """
    return time.strftime(timeformat,time.localtime(ts/1000))

def get_time(format="%Y-%m-%d %H:%M:%S") -> str:
    """
    获取当前时间的方法，格式根据format确定
    :param format: 时间格式
    :return: 时间字符串
    """
    return time.strftime(format,time.localtime())

def get_today(format="%Y-%m-%d") -> str:
    """
    获取当天日期
    :param format: 时间格式
    :return: 时间字符串
    """
    return get_time(format)