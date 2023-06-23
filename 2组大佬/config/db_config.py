# coding：utf8
"""
数据库相关配置

"""
#######logger相关配置##########################
# target
target_logger_table_name = 'logger'     # 存储数据表
target_logger_cols = "id int auto_increment primary key," \
                     "logger_time    VARCHAR(255) COMMENT '时间', " \
                     "level          VARCHAR(255) COMMENT '日志级别', " \
                     "file           VARCHAR(255) COMMENT '文件', " \
                     "respone_time   int          COMMENT'响应时间（毫秒）', " \
                     "province       VARCHAR(255) COMMENT '省份', " \
                     "city           VARCHAR(255) COMMENT '城市', " \
                     "comment        VARCHAR(255) COMMENT '说明'"
# metadata
metadata_logger_processed_table_name = 'logger_processed_table'  # 元数据表
metadata_logger_processed_table_create_cols_define = f"id int auto_increment primary key," \
                                                     f"path varchar(255)," \
                                                     f"processed_date varchar(255)"

###################### source相关配置
source_db_name = 'source'
source_host = 'localhost'
source_port = 3306
source_user = 'root'
source_passwd = 'root'
source_charset = 'utf8'

# source_metadata


# source_target
source_barcode_table_name = "barcode"



############## orders,orders_detail
# 元数据相关配置
metadata_db_name = 'metadata'
metadata_host = 'localhost'
metadata_port = 3306
metadata_user = 'root'
metadata_passwd = 'root'
metadata_charset = 'utf8'

metadata_orders_processed_table_name = 'orders_processed_table'  # 元数据表
metadata_barcode_processed_table_name = 'barcode_processed_table'  # 元数据表


metadata_orders_processed_table_create_cols_define = "" \
                                                     f"id int auto_increment primary key," \
                                                     f"path varchar(255)," \
                                                     f"processed_date varchar(255)"



# target相关配置
target_orders_table_name = "orders"  # 订单表
target_orders_detail_table_name = "orders_detail"  # 订单详细表
target_db_name = 'target'
target_host = 'localhost'
target_port = 3306
target_user = 'root'
target_passwd = 'root'
target_charset = 'utf8'
target_orders_cols = "store_id                    INT COMMENT '店铺ID'," \
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
                      "discount_rate               DECIMAL(20, 5) COMMENT '折扣率'," \
                      "discount_type               TINYINT COMMENT '折扣类型'," \
                      "discount                    DECIMAL(20, 5) COMMENT '折扣金额'," \
                      "money_before_whole_discount DECIMAL(20, 5) COMMENT '折扣前总金额'," \
                      "receivable                  DECIMAL(20, 5) COMMENT '应收金额'," \
                      "erase                       DECIMAL(20, 5) COMMENT '抹零金额'," \
                      "small_change                DECIMAL(20, 5) COMMENT '找零金额'," \
                      "total_no_discount           DECIMAL(20, 5) COMMENT '总价格(无折扣)'," \
                      "pay_total                   DECIMAL(20, 5) COMMENT '付款金额'," \
                      "pay_type                    VARCHAR(10) COMMENT '付款类型'," \
                      "payment_channel             TINYINT COMMENT '付款通道'," \
                      "payment_scenarios           VARCHAR(15) COMMENT '付款描述(无用)'," \
                      "product_count               INT COMMENT '本单卖出多少商品'," \
                      "date_ts                     VARCHAR(255) COMMENT '订单时间'," \
                      "INDEX (receivable)," \
                      "INDEX (date_ts)," \
                      "order_id                    VARCHAR(255) PRIMARY KEY"

target_orders_detail_cols = "order_id     VARCHAR(255) COMMENT '订单ID', " \
                            "barcode      VARCHAR(255) COMMENT '商品条码', " \
                            "name         VARCHAR(255) COMMENT '商品名称', " \
                            "count        INT COMMENT '本单此商品卖出数量', " \
                            "price_per    DECIMAL(20, 5) COMMENT '实际售卖单价', " \
                            "retail_price DECIMAL(20, 5) COMMENT '零售建议价', " \
                            "trade_price  DECIMAL(20, 5) COMMENT '贸易价格(进货价)', " \
                            "category_id  INT COMMENT '商品类别ID', " \
                            "unit_id      INT COMMENT '商品单位ID(包、袋、箱、等)', " \
                            "PRIMARY KEY (order_id, barcode)"


# 测试相关配置
unittest_db_name = 'unittest'
unittest_host = 'localhost'
unittest_port = 3306
unittest_user = 'root'
unittest_passwd = 'root'
unittest_charset = 'utf8'


