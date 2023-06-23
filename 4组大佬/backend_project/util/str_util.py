def check_null(data) -> bool:
    """
    空值转换，将无意义的数据转换成其他值
    :param data: 被判断的数据
    :return: True无意义，False有意义
    """
    if data == '':
        return True
    data_low = str(data).lower()
    if data_low == 'null' or data_low == 'none' or data_low == 'undefined':
        return True
    return False

def check_null_transform_to_str(data) -> str:
    """
    检查字符串数据是否有意义，有意义则返回字符串，在变量外加''，无意义则返回'NULL'
    :param data: 被判断的数据
    :return: 有意义'data',无意义'NULL'
    """
    if check_null(data):
        return 'NULL'
    return "'" + str(data) + "'"

def unite_path_slash(path: str) -> str:
    """
    将路径中的所有斜杠都规划为单左斜杠
    :param path: 被处理的路径字符串
    :return: 处理好的路径字符串
    """
    return path.replace('\\\\','/').replace('\\','/').replace('//','/')

