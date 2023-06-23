import json

stu_dict = {
    "name": 'aaa',
    "age": 12,
    "hobby": ["sing", "dance", "rap", "basketball"]
}

stu_str = '{"name": "aaa","age": 12,"hobby": ["sing", "dance", "rap", "basketball"]}'

# 将字典转为字符串
# 如果字典内有参数，可以使用ensure_ascii=False确保中文不乱码
stu_dict2str = json.dumps(stu_dict, ensure_ascii=False)
print(stu_dict2str)
print(type(stu_dict2str))

# 将字符串转为字典
# json字符串的引号必须是双引号，否则无法解析
stu_str2dict = json.loads(stu_str)
print(stu_str2dict)
print(type(stu_str2dict))


