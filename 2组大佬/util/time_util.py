# coding:utf-8
"""
时间工具包
"""
import time
import datetime


def get_time(formatter="%Y-%m-%d %H:%M:%S") -> str:
    """
    获取当前时间，格式
    :param formatter:
    :return:
    """
    return time.strftime(formatter, time.localtime())

def get_today(formatter="%Y-%m-%d") -> str:
    """
    获取当前时间，格式
    :param formatter:
    :return:
    """
    return get_time(formatter)


def second_ts_to_date_str(ts, formatter="%Y-%m-%d %H:%M:%S") -> str:
    """
    秒级时间戳转日期字符串
    :param ts: 秒级时间戳
    :param formatter: 日期格式
    :return: 日期时间串
    """
    return time.strftime(formatter, time.localtime(ts))


def millisecond_ts_to_date_str(ts, formatter="%Y-%m-%d %H:%M:%S") -> str:
    """
    微秒级时间戳转日期字符串
    :param ts: 秒级时间戳
    :param formatter: 日期格式
    :return: 日期时间串
    """
    return time.strftime(formatter, time.localtime(ts / 1000))

def str_to_time(time_str):
    """
    将含有年月日时分秒毫秒的时间字符串，去除毫秒，保留年月日时分秒
    :param time_str:
    :return:
    """
    dt_obj = datetime.datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S.%f")
    formatted_time_str = dt_obj.strftime("%Y-%m-%d %H:%M:%S")
    return formatted_time_str
