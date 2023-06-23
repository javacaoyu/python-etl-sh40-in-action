import json
import sys

import pymysql
import os
from waterwall.util import *

# 配置信息段
metadata_processed_table_name = 'orders_processed_files'
orders_json_file_data_path = "E:/pyetl-data"  # json文件夹再此目录下
target_orders_table_name = 'orders'
target_orders_detail_table_name = 'orders_detail'
batch_commit_counter = 1000
csv_output_root_path = "E:/pyetl-output-data"  # csv数据输出根目录
csv_output_sep = ','  # csv数据输出的分隔符定义

#


# todo step1元数据读取
# 1.1 构建数据库连接
metadata_conn: pymysql.Connection = pymysql.Connect(
    host='127.0.0.1',  # 主机
    port=3306,  # 端口
    user='root',  # 用户名
    password='123456',  # 密码
    charset='utf8',  # 编码
    autocommit=False,  # 是否自动提交
    db='metadata'
)

target_conn: pymysql.Connection = pymysql.Connect(
    host='127.0.0.1',
    port=3306,
    user='root',
    password='123456',
    charset='utf8',
    autocommit=False,
    db='target'
)

meta_cursor = metadata_conn.cursor()
target_cursor = target_conn.cursor()

# 1.2 判断元数据表是否存在
meta_cursor.execute("show tables")
if (metadata_processed_table_name,) not in meta_cursor.fetchall():
    # 不存在
    create_table_sql = f"create table if not exists {metadata_processed_table_name}(" \
                       f"id int primary key auto_increment comment '主键ID'," \
                       f"path varchar(255) comment '文件路径'," \
                       f"processed_date varchar(255) comment '记录日期')"
    print(f"元数据表：{metadata_processed_table_name}不存在，创建SQL语句：{create_table_sql}")
    meta_cursor.execute(create_table_sql)
else:
    # 存在
    pass

# 1.3 表存在，执行查询
meta_cursor.execute(f"select path from {metadata_processed_table_name}")
processed_file_list = []  # 记录以及处理过的文件路径列表
for line_tuple in meta_cursor.fetchall():
    processed_file_path = line_tuple[0]
    processed_file_list.append(processed_file_path)  # 已被处理的文件路径列表

# todo step2读取数据文件夹内的数据文件列表
all_files_list = []
for name in os.listdir(orders_json_file_data_path):
    # 路径统一化处理
    file_absolute_path = orders_json_file_data_path + "/" + name
    file_absolute_path = unite_path_slash(file_absolute_path)
    all_files_list.append(file_absolute_path)

# todo step3和元数据进行对比，找出本次需要处理的文件
need_to_process_files_list = []  # 需要被处理的文件路径列表
for path in all_files_list:
    if path not in processed_file_list:
        need_to_process_files_list.append(path)  # 需要被处理的文件路径列表
print(f"本次需要被处理的文件{need_to_process_files_list}")
if len(need_to_process_files_list) == 0:
    print(f"本次没有要处理的数据，程序停止")
    sys.exit(0)

# todo step4读取数据文件（JSON字符串数据），转换成字典，封装到list
origin_data_list = []  # 未清洗转换的数据字典列表
for path in need_to_process_files_list:
    for line in open(path, 'r', encoding='utf8').readlines():
        line = line.strip()  # 通过strip()方法去除空格以及换行符
        line_dict = json.loads(line)
        origin_data_list.append(line_dict)

# todo step5数据清洗转换
optimized_data_list = []  # 清洗转换后的list
for d in origin_data_list:
    # 省市区数据清洗
    if check_null(d['storeProvince']):
        # 无意义
        d['storeProvince'] = '未知省份'
    if check_null(d['storeCity']):
        # 无意义
        d['storeProvince'] = '未知城市'
    if check_null(d['storeDistrict']):
        # 无意义
        d['storeProvince'] = '未知行政区'

    optimized_data_list.append(d)
# print(optimized_data_list)

# todo step6数据写出
# 写出到MySQL
# 6.1组装SQL语句
orders_insert_sql_list = []
orders_detail_insert_sql_list = []

for d in optimized_data_list:
    # 封装orders_insert_sql_list
    sql = f"INSERT INTO {target_orders_table_name}(" \
          f"order_id,store_id,store_name,store_status,store_own_user_id," \
          f"store_own_user_name,store_own_user_tel,store_category," \
          f"store_address,store_shop_no,store_province,store_city," \
          f"store_district,store_gps_name,store_gps_address," \
          f"store_gps_longitude,store_gps_latitude,is_signed," \
          f"operator,operator_name,face_id,member_id,store_create_date_ts," \
          f"origin,day_order_seq,discount_rate,discount_type,discount," \
          f"money_before_whole_discount,receivable,erase,small_change," \
          f"total_no_discount,pay_total,pay_type,payment_channel," \
          f"payment_scenarios,product_count,date_ts" \
          f") VALUES(" \
          f"\'{d['orderID']}\', " \
          f"{d['storeID']}, " \
          f"{check_null_and_transform_to_sql_null(d['storeName'])}, " \
          f"{check_null_and_transform_to_sql_null(d['storeStatus'])}, " \
          f"{d['storeOwnUserId']}, " \
          f"{check_null_and_transform_to_sql_null(d['storeOwnUserName'])}, " \
          f"{check_null_and_transform_to_sql_null(d['storeOwnUserTel'])}, " \
          f"{check_null_and_transform_to_sql_null(d['storeCategory'])}, " \
          f"{check_null_and_transform_to_sql_null(d['storeAddress'])}, " \
          f"{check_null_and_transform_to_sql_null(d['storeShopNo'])}, " \
          f"{check_null_and_transform_to_sql_null(d['storeProvince'])}, " \
          f"{check_null_and_transform_to_sql_null(d['storeCity'])}, " \
          f"{check_null_and_transform_to_sql_null(d['storeDistrict'])}, " \
          f"{check_null_and_transform_to_sql_null(d['storeGPSName'])}, " \
          f"{check_null_and_transform_to_sql_null(d['storeGPSAddress'])}, " \
          f"{check_null_and_transform_to_sql_null(d['storeGPSLongitude'])}, " \
          f"{check_null_and_transform_to_sql_null(d['storeGPSLatitude'])}, " \
          f"{d['isSigned']}, " \
          f"{check_null_and_transform_to_sql_null(d['operator'])}, " \
          f"{check_null_and_transform_to_sql_null(d['operatorName'])}, " \
          f"{check_null_and_transform_to_sql_null(d['faceID'])}, " \
          f"{check_null_and_transform_to_sql_null(d['memberID'])}, " \
          f"'{millisecond_ts_to_date_str(d['storeCreateDateTS'])}', " \
          f"{check_null_and_transform_to_sql_null(d['origin'])}, " \
          f"{d['dayOrderSeq']}, " \
          f"{d['discountRate']}, " \
          f"{d['discountType']}, " \
          f"{d['discount']}, " \
          f"{d['moneyBeforeWholeDiscount']}, " \
          f"{d['receivable']}, " \
          f"{d['erase']}, " \
          f"{d['smallChange']}, " \
          f"{d['totalNoDiscount']}, " \
          f"{d['payedTotal']}, " \
          f"{check_null_and_transform_to_sql_null(d['payType'])}, " \
          f"{d['paymentChannel']}, " \
          f"{check_null_and_transform_to_sql_null(d['paymentScenarios'])}, " \
          f"{d['productCount']}, " \
          f"'{millisecond_ts_to_date_str(d['dateTS'])}'" \
          f")"
    orders_insert_sql_list.append(sql)
for d in optimized_data_list:
    # 封装orders_detail_insert_sql_list
    for product_dict in d['product']:
        sql = f"INSERT INTO {target_orders_detail_table_name}(" \
              f"order_id, barcode, name, count, price_per, retail_price, " \
              f"trade_price, category_id, unit_id) VALUES(" \
              f"\'{d['orderID']}\', " \
              f"\'{product_dict['barcode']}\', " \
              f"\'{product_dict['name']}\', " \
              f"{product_dict['count']}, " \
              f"{product_dict['pricePer']}, " \
              f"{product_dict['retailPrice']}, " \
              f"{product_dict['tradePrice']}, " \
              f"{product_dict['categoryID']}, " \
              f"{product_dict['unitID']}" \
              f")"
        orders_detail_insert_sql_list.append(sql)

# 6.2判断目标表是否存在，不存在，创建
current_tables_list = []
target_cursor.execute("show tables")
for line_tuple in target_cursor.fetchall():
    current_tables_list.append(line_tuple[0])

if target_orders_table_name not in current_tables_list:
    create_table_sql = f"CREATE TABLE IF NOT EXISTS {target_orders_table_name}(" \
                       "order_id                    VARCHAR(255) PRIMARY KEY," \
                       "store_id                    INT COMMENT '店铺ID'," \
                       "store_name                  VARCHAR(30) COMMENT '店铺名称'," \
                       "store_status                VARCHAR(10) COMMENT '店铺状态(open,close)'," \
                       "store_own_user_id           INT COMMENT '店主id'," \
                       "store_own_user_name         VARCHAR(50) COMMENT '店主名称'," \
                       "store_own_user_tel          VARCHAR(15) COMMENT '店主手机号'," \
                       "store_category              VARCHAR(10) COMMENT '店铺类型(normal,test)'," \
                       "store_address               VARCHAR(255) COMMENT '店铺地址'," \
                       "store_shop_no               VARCHAR(255) COMMENT '店铺第三方支付id号'," \
                       "store_province              VARCHAR(10) COMMENT '店铺所在省'," \
                       "store_city                  VARCHAR(10) COMMENT '店铺所在市'," \
                       "store_district              VARCHAR(10) COMMENT '店铺所在行政区'," \
                       "store_gps_name              VARCHAR(255) COMMENT '店铺gps名称'," \
                       "store_gps_address           VARCHAR(255) COMMENT '店铺gps地址'," \
                       "store_gps_longitude         VARCHAR(255) COMMENT '店铺gps经度'," \
                       "store_gps_latitude          VARCHAR(255) COMMENT '店铺gps纬度'," \
                       "is_signed                   TINYINT COMMENT '是否第三方支付签约(0,1)'," \
                       "operator                    VARCHAR(10) COMMENT '操作员'," \
                       "operator_name               VARCHAR(50) COMMENT '操作员名称'," \
                       "face_id                     VARCHAR(255) COMMENT '顾客面部识别ID'," \
                       "member_id                   VARCHAR(255) COMMENT '顾客会员ID'," \
                       "store_create_date_ts        TIMESTAMP COMMENT '店铺创建时间'," \
                       "origin                      VARCHAR(255) COMMENT '原始信息(无用)'," \
                       "day_order_seq               INT COMMENT '本订单是当日第几单'," \
                       "discount_rate               DECIMAL(10, 5) COMMENT '折扣率'," \
                       "discount_type               TINYINT COMMENT '折扣类型'," \
                       "discount                    DECIMAL(10, 5) COMMENT '折扣金额'," \
                       "money_before_whole_discount DECIMAL(10, 5) COMMENT '折扣前总金额'," \
                       "receivable                  DECIMAL(10, 5) COMMENT '应收金额'," \
                       "erase                       DECIMAL(10, 5) COMMENT '抹零金额'," \
                       "small_change                DECIMAL(10, 5) COMMENT '找零金额'," \
                       "total_no_discount           DECIMAL(10, 5) COMMENT '总价格(无折扣)'," \
                       "pay_total                   DECIMAL(10, 5) COMMENT '付款金额'," \
                       "pay_type                    VARCHAR(10) COMMENT '付款类型'," \
                       "payment_channel             TINYINT COMMENT '付款通道'," \
                       "payment_scenarios           VARCHAR(15) COMMENT '付款描述(无用)'," \
                       "product_count               INT COMMENT '本单卖出多少商品'," \
                       "date_ts                     VARCHAR(255) COMMENT '订单时间'," \
                       "INDEX (receivable)," \
                       "INDEX (date_ts))"
    target_cursor.execute(create_table_sql)
if target_orders_detail_table_name not in current_tables_list:
    create_table_sql = f"CREATE TABLE IF NOT EXISTS {target_orders_detail_table_name}(" \
                       "order_id     VARCHAR(255) COMMENT '订单ID', " \
                       "barcode      VARCHAR(255) COMMENT '商品条码', " \
                       "name         VARCHAR(255) COMMENT '商品名称', " \
                       "count        INT COMMENT '本单此商品卖出数量', " \
                       "price_per    DECIMAL(10, 5) COMMENT '实际售卖单价', " \
                       "retail_price DECIMAL(10, 5) COMMENT '零售建议价', " \
                       "trade_price  DECIMAL(10, 5) COMMENT '贸易价格(进货价)', " \
                       "category_id  INT COMMENT '商品类别ID', " \
                       "unit_id      INT COMMENT '商品单位ID(包、袋、箱、等)', " \
                       "PRIMARY KEY (order_id, barcode))"
    target_cursor.execute(create_table_sql)

# 6.3执行SQL插入操作，走批量操作
i = 0
j = 0
for sql in orders_insert_sql_list:
    target_cursor.execute(sql)
    i += 1
    if i % batch_commit_counter == 0:
        target_conn.commit()
        print(f"orders表已插入{i}条数据")

for sql in orders_detail_insert_sql_list:
    target_cursor.execute(sql)
    j += 1
    if j % batch_commit_counter == 0:
        target_conn.commit()
        print(f"orders_detail表已插入{j}条数据")
target_conn.commit()
print(f"orders表一共插入{i}条数据")
print(f"orders_detail表一共插入{j}条数据")

# todo step7写出到CSV文件
# 7.1 准备文件对象
orders_csv_output_path = f"{csv_output_root_path}/orders_{get_time('%Y%m%d_%H%M%S')}.csv"
orders_detail_csv_output_path = f"{csv_output_root_path}/orders_detail_{get_time('%Y%m%d_%H%M%S')}.csv"
orders_csv_writer = open(orders_csv_output_path, 'a', encoding='utf8')
orders_detail_csv_writer = open(orders_detail_csv_output_path, 'a', encoding='utf8')

# 7.2先写第一行(csv第一行)
orders_header_str = \
            f"discountRate{csv_output_sep}" \
            f"storeShopNo{csv_output_sep}" \
            f"dayOrderSeq{csv_output_sep}" \
            f"storeDistrict{csv_output_sep}" \
            f"isSigned{csv_output_sep}" \
            f"storeProvince{csv_output_sep}" \
            f"origin{csv_output_sep}" \
            f"storeGPSLongitude{csv_output_sep}" \
            f"discount{csv_output_sep}" \
            f"storeID{csv_output_sep}" \
            f"productCount{csv_output_sep}" \
            f"operatorName{csv_output_sep}" \
            f"operator{csv_output_sep}" \
            f"storeStatus{csv_output_sep}" \
            f"storeOwnUserTel{csv_output_sep}" \
            f"payType{csv_output_sep}" \
            f"discountType{csv_output_sep}" \
            f"storeName{csv_output_sep}" \
            f"storeOwnUserName{csv_output_sep}" \
            f"dateTS{csv_output_sep}" \
            f"smallChange{csv_output_sep}" \
            f"storeGPSName{csv_output_sep}" \
            f"erase{csv_output_sep}" \
            f"storeGPSAddress{csv_output_sep}" \
            f"orderID{csv_output_sep}" \
            f"moneyBeforeWholeDiscount{csv_output_sep}" \
            f"storeCategory{csv_output_sep}" \
            f"receivable{csv_output_sep}" \
            f"faceID{csv_output_sep}" \
            f"storeOwnUserId{csv_output_sep}" \
            f"paymentChannel{csv_output_sep}" \
            f"paymentScenarios{csv_output_sep}" \
            f"storeAddress{csv_output_sep}" \
            f"totalNoDiscount{csv_output_sep}" \
            f"payedTotal{csv_output_sep}" \
            f"storeGPSLatitude{csv_output_sep}" \
            f"storeCreateDateTS{csv_output_sep}" \
            f"storeCity{csv_output_sep}" \
            f"memberID"
orders_csv_writer.write(orders_header_str)
orders_csv_writer.write("\n")

orders_detail_header_str = \
            f"orderID{csv_output_sep}" \
            f"barcode{csv_output_sep}" \
            f"count{csv_output_sep}" \
            f"name{csv_output_sep}" \
            f"unitID{csv_output_sep}" \
            f"pricePer{csv_output_sep}" \
            f"retailPrice{csv_output_sep}" \
            f"tradePrice{csv_output_sep}" \
            f"categoryID"
orders_detail_csv_writer.write(orders_detail_header_str)
orders_detail_csv_writer.write("\n")

# 7.3写数据
i = 0
j = 0
for d in optimized_data_list:
    i += 1
    csv_line = \
            f"{d['discountRate']}{csv_output_sep}" \
            f"{d['storeShopNo']}{csv_output_sep}" \
            f"{d['dayOrderSeq']}{csv_output_sep}" \
            f"{d['storeDistrict']}{csv_output_sep}" \
            f"{d['isSigned']}{csv_output_sep}" \
            f"{d['storeProvince']}{csv_output_sep}" \
            f"{d['origin']}{csv_output_sep}" \
            f"{d['storeGPSLongitude']}{csv_output_sep}" \
            f"{d['discount']}{csv_output_sep}" \
            f"{d['storeID']}{csv_output_sep}" \
            f"{d['productCount']}{csv_output_sep}" \
            f"{d['operatorName']}{csv_output_sep}" \
            f"{d['operator']}{csv_output_sep}" \
            f"{d['storeStatus']}{csv_output_sep}" \
            f"{d['storeOwnUserTel']}{csv_output_sep}" \
            f"{d['payType']}{csv_output_sep}" \
            f"{d['discountType']}{csv_output_sep}" \
            f"{d['storeName']}{csv_output_sep}" \
            f"{d['storeOwnUserName']}{csv_output_sep}" \
            f"{d['dateTS']}{csv_output_sep}" \
            f"{d['smallChange']}{csv_output_sep}" \
            f"{d['storeGPSName']}{csv_output_sep}" \
            f"{d['erase']}{csv_output_sep}" \
            f"{d['storeGPSAddress']}{csv_output_sep}" \
            f"{d['orderID']}{csv_output_sep}" \
            f"{d['moneyBeforeWholeDiscount']}{csv_output_sep}" \
            f"{d['storeCategory']}{csv_output_sep}" \
            f"{d['receivable']}{csv_output_sep}" \
            f"{d['faceID']}{csv_output_sep}" \
            f"{d['storeOwnUserId']}{csv_output_sep}" \
            f"{d['paymentChannel']}{csv_output_sep}" \
            f"{d['paymentScenarios']}{csv_output_sep}" \
            f"{d['storeAddress']}{csv_output_sep}" \
            f"{d['totalNoDiscount']}{csv_output_sep}" \
            f"{d['payedTotal']}{csv_output_sep}" \
            f"{d['storeGPSLatitude']}{csv_output_sep}" \
            f"{d['storeCreateDateTS']}{csv_output_sep}" \
            f"{d['storeCity']}{csv_output_sep}" \
            f"{d['memberID']}"
    orders_csv_writer.write(csv_line)
    orders_csv_writer.write("\n")

for d in optimized_data_list:
    for product_dict in d["product"]:
        j += 1
        csv_line = \
            f"{d['orderID']}{csv_output_sep}" \
            f"{product_dict['barcode']}{csv_output_sep}" \
            f"{product_dict['count']}{csv_output_sep}" \
            f"{product_dict['name']}{csv_output_sep}" \
            f"{product_dict['unitID']}{csv_output_sep}" \
            f"{product_dict['pricePer']}{csv_output_sep}" \
            f"{product_dict['retailPrice']}{csv_output_sep}" \
            f"{product_dict['tradePrice']}{csv_output_sep}" \
            f"{product_dict['categoryID']}"
        orders_detail_csv_writer.write(csv_line)
        orders_detail_csv_writer.write("\n")

# 7.4关闭文件对象
orders_csv_writer.close()
orders_detail_csv_writer.close()
print(f"orders的CSV文件写出完成，共写出{i}条数据")
print(f"orders_detail的CSV文件写出完成，共写出{j}条数据")


# todo step8记录元数据
for path in need_to_process_files_list:
    sql = f"insert into {metadata_processed_table_name} values (" \
          f"NULL, '{path}', '{get_time()}')"
    print(f"向元数据记录本次处理的文件是{path},SQL语句是{sql}")
    meta_cursor.execute(sql)
    metadata_conn.commit()

target_conn.close()
metadata_conn.close()
