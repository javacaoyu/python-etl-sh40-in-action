# coding:utf8
"""
文件相关工具方法
"""
import os
from util import str_util

import re

from config import project_config


def get_new_by_two_list_compera(big_list, small_list):
    tmp_list = []
    for i in big_list:
        if i not in small_list:
            tmp_list.append(i)
    return tmp_list


def get_all_file_list(path=project_config.orders_json_file_data_path, recursion=False):
    list1 = os.listdir(path)
    result_list = []
    for i in list1:
        absolute_path = str_util.unite_path_slash(path+'/'+i)
        if os.path.isfile(absolute_path):
            result_list.append(absolute_path)
        else:
            if recursion:
                recursion_result = get_all_file_list(absolute_path)
                result_list += recursion_result

    return result_list


def get_file_content(path=project_config.orders_json_file_data_path):
    """
    获取文件内容
    :param path: 文件路径
    :return: list
    """
    list1 = []
    for i in get_all_file_list(path):
        for line in open(i, 'r', encoding='UTF-8').readlines():
            line = line.strip()
            list1.append(line)
    for i in range(len(list1)):
        list1[i] = re.split(r"\t", list1[i])
    return list1

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