"""
各种工具方法，封装重复使用的函数功能
"""
import time


def check_null(data) -> bool:
    """
    检查传入的变量是否是无意义的内容。
    无意义：
    - 空字符串
    - Null
    - None
    - undefined
    :param data: 被判断的变量
    :return: True无意义  False有意义
    """
    if not data:
        # 如果data是None，直接返回无意义
        return True
    data = str(data)
    data = data.lower  # 统一转小写，避免大小写问题
    if data == "" or data == "null" or data == "none" or data == "undefined":
        return True
    return False


def check_null_and_transform_to_sql_null(data) -> str:
    """
    检查字符串内容是否是有意义，如果是返回NULL字符串，如果不是返回本身，同时外面包上''
    :param data: 被判断字符串
    :return: 字符串
    """
    if check_null(data):
        return "NULL"
    return "'" + str(data) + "'"


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


def unite_path_slash(path) -> str:
    """
    统一将路径的斜杠，规划为单左斜杠
    :param path:
    :return:
    """
    return path \
        .replace("\\\\", "/") \
        .replace("\\", "/") \
        .replace("//", "/")
