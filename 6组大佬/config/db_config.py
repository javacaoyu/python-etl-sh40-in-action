"""
和数据相关的配置项
"""

# 元数据相关数据库配置记录

# todo 元数据库相关
metadata_orders_processed_table_create_cols_define = f"" \
                       f"id int primary key auto_increment comment '主键ID'," \
                       f"path varchar(255) comment '文件路径'," \
                       f"processed_date varchar(255) comment '记录日期'"  # orders业务元数据

metadata_db_name = 'metadata'
metadata_processed_table_name = 'orders_processed_files'

metadata_barcode_processed_table_name = "barcode_update_time_record"                    # barcode业务元数据表名
metadata_barcode_processed_table_create_cols_define = f"id int auto_increment primary key, " \
                                                      f"last_update varchar(255), " \
                                                      f"processed_date varchar(255)"

metadata_host = "127.0.0.1"
metadata_port = 3306
metadata_user = "root"
metadata_password = "123456"
metadata_charset = "utf8"


# todo 目标库相关
target_orders_processed_table_create_cols_define = f"" \
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
                       "INDEX (date_ts)"

target_orders_detail_processed_table_create_cols_define = f"" \
                       "order_id     VARCHAR(255) COMMENT '订单ID', " \
                       "barcode      VARCHAR(255) COMMENT '商品条码', " \
                       "name         VARCHAR(255) COMMENT '商品名称', " \
                       "count        INT COMMENT '本单此商品卖出数量', " \
                       "price_per    DECIMAL(10, 5) COMMENT '实际售卖单价', " \
                       "retail_price DECIMAL(10, 5) COMMENT '零售建议价', " \
                       "trade_price  DECIMAL(10, 5) COMMENT '贸易价格(进货价)', " \
                       "category_id  INT COMMENT '商品类别ID', " \
                       "unit_id      INT COMMENT '商品单位ID(包、袋、箱、等)', " \
                       "PRIMARY KEY (order_id, barcode)"

target_barcode_processed_table_create_cols_define = "`code` varchar(50) NOT NULL," \
                                                    "`name` varchar(200) DEFAULT ''," \
                                                    "`spec` varchar(200) DEFAULT ''," \
                                                    "`trademark` varchar(100) DEFAULT ''," \
                                                    "`addr` varchar(200) DEFAULT ''," \
                                                    "`units` varchar(50) DEFAULT ''," \
                                                    "`factory_name` varchar(200) DEFAULT ''," \
                                                    "`trade_price` varchar(20) DEFAULT '0.0000'," \
                                                    "`retail_price` varchar(20) DEFAULT '0.0000'," \
                                                    "`updateAt` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP," \
                                                    "`wholeunit` varchar(50) DEFAULT NULL," \
                                                    "`wholenum` int(11) DEFAULT NULL," \
                                                    "`img` varchar(500) DEFAULT NULL," \
                                                    "`src` varchar(20) DEFAULT NULL," \
                                                    "PRIMARY KEY (`code`)"

target_orders_table_name = 'orders'
target_orders_detail_table_name = 'orders_detail'
target_db_name = 'target'
target_host = "127.0.0.1"
target_port = 3306
target_user = "root"
target_password = "123456"
target_charset = "utf8"

unittest_db_name = "unittest"
unittest_host = "127.0.0.1"
unittest_port = 3306
unittest_user = "root"
unittest_password = "123456"
unittest_charsets = "utf8"

# source_orders_detail_table_name = 'orders_detail'
# source_db_name = 'source'
# source_host = "127.0.0.1"
# source_port = 3306
# source_user = "root"
# source_password = "123456"
# source_charset = "utf8"

# ---------------------backend---------------------
metadata_backend_processed_table_name = "backend_processed_files"
target_backend_table_name = "backend"
metadata_backend_processed_table_create_cols_define = "id int primary key auto_increment," \
                                                      "path varchar(255)," \
                                                      "processed_date varchar(255)"
target_backend_processed_table_create_cols_define = "id int primary key auto_increment comment '主键id自增'," \
                                                    "backend_time varchar(255) comment '日志产生时间'," \
                                                    "backend_type varchar(255) comment '日志状态'," \
                                                    "file_name varchar(255) comment '文件名'," \
                                                    "response_time varchar(255) comment '响应时长'," \
                                                    "province varchar(255) comment '省份'," \
                                                    "city varchar(255) comment '城市'," \
                                                    "backend_info varchar(255) comment '日志信息'"
