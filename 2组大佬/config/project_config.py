#coding:utf8
"""
工程通用配置
"""
from day02.util.time_util import *

# 日志
source_logger_path = "D:/ETL2/code/day02/tmp/pyetl-data-backend-logs/"

# 订单
orders_json_file_data_path = "D:/ETL2/数据资料/test"  # 要处理的数据文件

# csv
csv_output_root_path = "D:\\ETL2\\数据资料\\csv"
csv_output_sep = ','
# 7.1 准备写出的文件对象
orders_csv_output_path = f"{csv_output_root_path}\\order_{get_time('%Y%m%d_%H%M%S')}.csv"
orders_detail_csv_output_path = f"{csv_output_root_path}\\order_detail_{get_time('%Y%m%d_%H%M%S')}.csv"
orders_csv_write = open(orders_csv_output_path, 'w', encoding="utf-8")
orders_detail_csv_write = open(orders_detail_csv_output_path, 'w', encoding="utf-8")

# 批量控制
batch_commit_counter = 1000  # 提交量