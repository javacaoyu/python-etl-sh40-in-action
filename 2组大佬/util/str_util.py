# coding:utf8
"""
字符串相关工具包
"""


def check_null(data: str) -> bool:
    """
    检查传入的变量是否是无意义内容
    -空字符串：
    -NULL：
    -None:
    -undefined:
    :param data:被判断的变量
    :return: True是无意义，False是有意义
    """
    if not data:
        # 如果data是None，直接返回True无意义
        return True

    # 同一大小写，都转小写
    data = str(data).lower()
    if data == "" or data == "null" or data == "none" or data == "undefined":
        return True
    return False


def check_null_and_transform_to_sql_null(data: str) -> str:
    """
    同一”“，none，null都为sql意义上的null
    :param data: 需要判断的数据
    :return: 有意义返回原数据+单引号，无意义返回‘null’
    """
    if check_null(data):
        return 'NULL'
    return "'" + str(data) + "'"


def unite_path_slash(path: str) -> str:
    """
    统一路径为单座斜杠
    :param path:
    :return:
    """
    return path.replace("\\\\", "/") \
        .replace("\\", "/") \
        .replace("//", "/")

def clean_str(data):
    """
    清楚字符串中的‘ “ $ # \ /
    :param data:
    :return:
    """
    return str(data).replace("\"","")\
        .replace("\'","")\
        .replace("$","")\
        .replace("\\","")\
        .replace("/","")\
        .replace("&","")\
        .replace("^","")\
        .replace(",","")\
        .replace("[","")\
        .replace("]","")

def clean_respone(data:str):
    data = data.strip("响应时间:").replace("ms","")
    return int(data)


