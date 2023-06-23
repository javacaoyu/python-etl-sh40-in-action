"""
字符串相关工具方法
"""


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
    data = str(data).lower()  # 统一转小写，避免大小写问题
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


if __name__ == '__main__':
    data = "NULL"
    data = str(data).lower()
    print(data)
    print(check_null(data))
