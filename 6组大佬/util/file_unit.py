"""
文件相关方法
"""
import os
from util import str_util


def get_new_by_two_list_compare(big_list, small_list):
    """
    获取big_list有，small_list没有
    :param big_list:
    :param small_list:
    :return: 新内容list
    """
    tmp_list = []
    for i in big_list:
        if i not in small_list:
            tmp_list.append(i)
    return tmp_list

def get_files_list(path, recursion=False):
    """
    递归查询文件夹内的所有文件
    :param path: 文件夹路径
    :param recursion: 是否递归 default=False 不递归
    :return: 文件绝对路径列表
    """
    result_list = []
    names = os.listdir(path)

    for name in names:
        absolute_path = str_util.unite_path_slash(path + "/" + name)
        if os.path.isfile(absolute_path):
            result_list.append(absolute_path)
        else:
            if recursion:
                recursion_result = get_files_list(absolute_path, recursion)
                result_list += recursion_result
    return result_list


def change_file_suffix(file_path, target_suffix, origin_suffix='.tmp'):
    """
    修改我呢见的后缀名
    :param file_path: 被修改的文件路径
    :param target_suffix: 目标后缀
    :param origin_suffix: 原始后缀
    :return:
    """
    new_path = file_path.replace(origin_suffix, target_suffix)
    os.rename(file_path, new_path)
