# coding:utf8
"""
和数据库相关的配置项
项目中会用到：
- metadata：元数据记录（库）
- target：目标记录（库）
"""

# ---------------------- 元数据相关数据库配置记录 ----------------------
metadata_orders_processed_table_name = \
    'orders_processed_files'                        # 订单（Json数据文件）采集业务元数据表的表名
metadata_orders_processed_table_create_cols_define = \
    f"id int auto_increment primary key, " \
    f"path varchar(255), " \
    f"processed_date varchar(255)"

metadata_barcode_processed_table_name = \
    "barcode_update_time_record"                    # barcode业务元数据表名
metadata_barcode_processed_table_create_cols_define = \
    f"id int auto_increment primary key, " \
    f"last_update varchar(255), " \
    f"processed_date varchar(255)"

metadata_db_name = 'metadata'
metadata_host = "192.168.88.100"
metadata_port = 3306
metadata_user = "root"
metadata_password = "123456"
metadata_charset = "UTF8"
# ----------------------   元数据相关数据库配置记录 ----------------------

# # ---------------------- 目标库相关数据配置记录   ----------------------
target_orders_table_name = 'orders'                 # 目标库订单表，表名
target_orders_table_cols_define = \
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
                          "INDEX (date_ts)"
target_orders_detail_table_name = 'orders_detail'   # 目标库订单表，表名
target_orders_detail_table_cols_define = \
                                "order_id     VARCHAR(255) COMMENT '订单ID', " \
                                "barcode      VARCHAR(255) COMMENT '商品条码', " \
                                "name         VARCHAR(255) COMMENT '商品名称', " \
                                "count        INT COMMENT '本单此商品卖出数量', " \
                                "price_per    DECIMAL(20, 5) COMMENT '实际售卖单价', " \
                                "retail_price DECIMAL(20, 5) COMMENT '零售建议价', " \
                                "trade_price  DECIMAL(20, 5) COMMENT '贸易价格(进货价)', " \
                                "category_id  INT COMMENT '商品类别ID', " \
                                "unit_id      INT COMMENT '商品单位ID(包、袋、箱、等)', " \
                                "PRIMARY KEY (order_id, barcode)"

target_barcode_table_name = "barcode"               # 目标库商品表，表名
target_barcode_table_cols_define = \
     "code           varchar(50) NOT NULL COMMENT '商品条码', " \
     "name           varchar(200) DEFAULT '' COMMENT '商品名称', " \
     "spec           varchar(200) DEFAULT '' COMMENT '商品规格', " \
     "trademark      varchar(100) DEFAULT '' COMMENT '商标', " \
     "addr           varchar(200) DEFAULT '' COMMENT '厂家地址', " \
     "units          varchar(50) DEFAULT '' COMMENT '单位', " \
     "factory_name   varchar(200) DEFAULT '' COMMENT '厂家名称', " \
     "trade_price    varchar(20) DEFAULT '0.0000' COMMENT '进价', " \
     "retail_price   varchar(20) DEFAULT '0.0000' COMMENT '零售价格', " \
     "update_at      timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间', " \
     "wholeunit      varchar(50) DEFAULT NULL COMMENT '计量单位', " \
     "wholenum       int(11) DEFAULT NULL," \
     "img            varchar(500) DEFAULT NULL COMMENT '图片', " \
     "src            varchar(20) DEFAULT NULL COMMENT '图片地址', " \
     "PRIMARY KEY (`code`)"

target_db_name = 'target'
target_host = "192.168.88.100"
target_port = 3306
target_user = "root"
target_password = "123456"
target_charset = "UTF8"
# # ---------------------- 目标库相关数据配置记录 ----------------------

# # ---------------------- 单元测试库相关 ----------------------
unittest_db_name = 'unittest'
unittest_host = "192.168.88.100"
unittest_port = 3306
unittest_user = "root"
unittest_password = "123456"
unittest_charset = "UTF8"
# # ---------------------- 单元测试库相关 ----------------------

# # ---------------------- 数据源数据库相关 ----------------------
source_db_name = 'source'
source_host = "192.168.88.100"
source_port = 3306
source_user = "root"
source_password = "123456"
source_charset = "UTF8"
source_barcode_table_name = "sys_barcode"       # 采集的数据库表名称
# # ---------------------- 数据源数据库相关 ----------------------
