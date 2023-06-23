# coding:utf8
"""
记录时间相关的工具代码
"""
import time


def get_time(formatter="%Y-%m-%d %H:%M:%S") -> str:
    """
    获取当前时间，格式基于传入参数formatter
    :param formatter: 时间格式
    :return: 时间字符串
    """
    return time.strftime(formatter, time.localtime())


def get_today(formatter="%Y-%m-%d") -> str:
    return get_time(formatter)


def second_ts_to_date_str(ts, formatter="%Y-%m-%d %H:%M:%S") -> str:
    """
    秒级时间戳转日期字符串
    :param ts: 被转换的时间戳数字
    :param formatter: 日期格式字符串定义
    :return: 日期字符串
    """
    return time.strftime(formatter, time.localtime(ts))


def millisecond_ts_to_date_str(ts, formatter="%Y-%m-%d %H:%M:%S") -> str:
    """
    毫秒级时间戳转日期字符串
    :param ts: 被转换的时间戳数字
    :param formatter: 日期格式字符串定义
    :return: 日期字符串
    """
    return time.strftime(formatter, time.localtime(ts / 1000))


from datetime import datetime


def extract_time(date_str, time_format="%Y-%m-%d %H:%M:%S"):
    """
    从日期时间字符串中提取特定的时间部分
    """
    date_obj = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
    time_str = date_obj.strftime(time_format)
    return time_str
