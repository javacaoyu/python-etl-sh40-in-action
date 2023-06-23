# todo 1与数据库建立关联
import json
import os

import pymysql
from util import *

#
base_dir = "E:/pyetl-data"
target_orders_table_name = 'orders'
target_orders_detail_table_name = 'orders_detail'

#


metadata_conn: pymysql.Connection = pymysql.Connect(
    host='127.0.0.1',
    user='root',
    password='123456',
    port=3306,
    charset='utf8',
    autocommit=False,
    db='metadata1'
)
target_conn: pymysql.Connection = pymysql.Connect(
    host='127.0.0.1',
    user='root',
    password='123456',
    port=3306,
    charset='utf8',
    autocommit=False,
    db='target1'
)
metadata_cursor = metadata_conn.cursor()
target_cursor = target_conn.cursor()

# todo 2读取元数据信息
metadata_processed_list = []
metadata_list = []

metadata_cursor.execute("show tables")
for item in metadata_cursor.fetchall():
    metadata_processed_list.append(item)  # 已经执行过的文件名称

for name in os.listdir(base_dir):
    if base_dir + '/' + name not in metadata_processed_list:
        metadata_list.append(base_dir + '/' + name)  # 要处理的文件路径列表

# todo 3取出数据
to_be_process_data_list = []
for path in metadata_list:
    for line in open(path, 'r', encoding='utf8').readlines():
        line = line.strip()
        line = json.loads(line)
        to_be_process_data_list.append(line)

print(to_be_process_data_list[0])

# todo 4省市区处理
to_be_process_data_changed_list = []
for d in to_be_process_data_list:
    if check_null(d.get('storeProvince')):
        d['storeProvince'] = "未知省份"
    if check_null(d.get('storeCity')):
        d['storeCity'] = "未知城市"
    if check_null(d.get('storeDistrict')):
        d['storeDistrict'] = "未知区"
    to_be_process_data_changed_list.append(d)

# todo 5组装sql
to_be_process_orders_sql_list = []
to_be_process_orders_datail_sql_list = []
for d in to_be_process_data_changed_list:
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
    to_be_process_orders_sql_list.append(sql)
for d in to_be_process_data_changed_list:
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
        to_be_process_orders_datail_sql_list.append(sql)
print(to_be_process_orders_sql_list)
print(to_be_process_orders_datail_sql_list)

target_cursor.execute("show tables")
orders_process_table_list = []
for item in target_cursor.fetchall():
    orders_process_table_list.append(item)
if target_orders_table_name not in orders_process_table_list:
    sql = f"CREATE TABLE {target_orders_table_name}(" \
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
    target_cursor.execute(sql)
if target_orders_detail_table_name not in orders_process_table_list:
    sql = f"CREATE TABLE {target_orders_detail_table_name}(" \
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
    target_cursor.execute(sql)

# todo 6执行
i = 0
j = 0
for sql in to_be_process_orders_sql_list:
    target_cursor.execute(sql)
    i += 1
    if i % 1000 == 0:
        target_conn.commit()
        print(f"orders已插入{i}条数据")

for sql in to_be_process_orders_datail_sql_list:
    target_cursor.execute(sql)
    j += 1
    if j % 1000 == 0:
        target_conn.commit()
        print(f"orders_detail已插入{j}条数据")
target_conn.commit()
print(f"orders执行完毕，一共插入数据{i}条")
print(f"orders_detail执行完毕，一共插入数据{j}条")
