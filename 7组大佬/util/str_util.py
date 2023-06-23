# coding:utf8
"""
字符串相关工具方法
"""
import re


def check_null(data):
    if not data:
        return True
    if str(data).lower() in ("", "null", "none", "undefined"):
        return True
    return False


# 检查字符串内容有误意义
def check_null_and_transform_to_sql_null(data):
    """
    :param data:
    :return: null字符串或data本身加上''
    """
    if check_null(data):
        return "null"
    else:
        return "'" + str(data) + "'"


# 处理文件路径
def unite_path_slash(path: str) -> str:
    return path \
        .replace("\\\\", "/") \
        .replace("\\", "/") \
        .replace("//", "/")


def replace_comma(data: str):
    return data.replace(",", "，")


def remove_fist_last(data: str):
    return data[1:-1]


def remove_millisecond(data):
    return data[:data.rfind(".")]


def fetch_number(data):
    return int(re.findall("[0-9]+", data)[0])
