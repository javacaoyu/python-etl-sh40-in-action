import time


def check_null(data) -> bool:
    """
    检查传入数据是否是无意义的内容
    :param data:
    :return:
    """
    if not data:
        return True
    data = str(data)
    data = data.lower()
    if data == 'null' or data == 'none' or data == '' or data == 'undefined':
        return True
    return False


def check_null_and_transform_to_sql_null(data) -> str:
    """

    :param data:
    :return:
    """
    if check_null(data):
        return 'NULL'
    return "'" + str(data) + "'"


def second_ts_to_date_str(dt, formatter="%Y-%m-%d %H:%M:%S"):
    """

    :param dt:
    :param formatter:
    :return:
    """
    return time.strftime(formatter, time.localtime(dt))


def millisecond_ts_to_date_str(dt, formatter="%Y-%m-%d %H:%M:%S"):
    """

    :param dt:
    :param formatter:
    :return:
    """
    return time.strftime(formatter, time.localtime(dt/1000))
