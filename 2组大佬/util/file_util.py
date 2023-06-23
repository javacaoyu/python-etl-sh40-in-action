# coding:utf8
"""
文件相关工具方法
"""
import os
from day02.util.str_util import *

def get_new_by_two_list_compare(big_list, small_list):
    """
    获取big_list中有的,small_list中没有的
    :param big_list: 内容多的
    :param small_list: 内容少的
    :return: 新内容的list
    """
    tmp_list = []
    for i in big_list:
        if i not in small_list:
            tmp_list.append(i)
    return tmp_list


def get_file_list(path):
    result_list = []
    names = os.listdir(path)

    for name in names:
        # 组装全路径,并统一路径,防止path内原本尾部自带/
        absolute_path = unite_path_slash(path+"/"+name)
        # 判断是否是文件
        if os.path.isfile(absolute_path):
            # 是文件
            result_list.append(absolute_path)
        else:
            # 不是文件,走递归,重新组装其实目录
            #
            res_list = get_file_list(absolute_path)
            result_list += res_list
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