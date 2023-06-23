# coding:utf8
"""
文件相关工具方法
"""
import os
from util import str_util


def get_new_by_two_list_compare(big_list, small_list):
    """
    获取big_list中有的，small_list中没有的
    :param big_list: 应当是内容多的那一个
    :param small_list: 应当是内容少的那一个
    :return: 新内容的list
    """
    tmp_list = []
    for i in big_list:
        if i not in small_list:
            tmp_list.append(i)
    return tmp_list


def get_files_list(path, recursion=False):
    result_list = []
    for name in os.listdir(path):
        absolute_path = str_util.unite_path_slash(path + '/' + name)
        if os.path.isfile(absolute_path):
            result_list.append(absolute_path)
        else:
            if recursion:
                result_list += get_files_list(absolute_path)
    return result_list


def change_file_suffix(file_path: str, target_suffix, origin_suffix='.tmp'):
    """
    修改文件的后缀名
    :param file_path: 被修改的文件全路径
    :param target_suffix: 目标后缀
    :param origin_suffix: 原始后缀，默认是.tmp
    :return: None
    """
    new_path = file_path.replace(origin_suffix, target_suffix)
    os.rename(file_path, new_path)
