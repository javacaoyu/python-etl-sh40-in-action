# coding:utf8
"""
和数据库相关的配置项
项目中会用到：
- metadata：元数据记录（库）
- target：目标记录（库）
"""

# 元数据相关的数据库配置记录
metadata_logs_processed_table_name = 'logs_processed_files'       # 记录元数据的表名
metadata_logs_processed_table_create_cols_define = \
    f"id int auto_increment primary key, " \
    f"path varchar(255), " \
    f"processed_date varchar(255)"

# 目标库相关数据配置记录
target_logs_data_table_name = 'logs_data'                           # 日志数据表名
# 目标表列构建
target_logs_table_cols_define = "logs_id        int auto_increment  primary key," \
                                "data_ts        varchar(50)    ," \
                                "log_level      varchar(20)    ," \
                                "log_module     varchar(50)    ," \
                                "response_time  varchar(50)    ," \
                                "province       varchar(50)    ," \
                                "city           varchar(50)    ," \
                                "log_msg        varchar(255)   "

# 元数据相关数据库配置记录
metadata_db_name = 'metadata'
metadata_host = "localhost"
metadata_port = 3306
metadata_user = "root"
metadata_password = "123456"
metadata_charset = "UTF8"

# 目标库相关数据配置记录
target_db_name = 'target'
target_host = "localhost"
target_port = 3306
target_user = "root"
target_password = "123456"
target_charset = "UTF8"

# 测试库相关数据配置记录
unittest_db_name = 'unittest'
unittest_host = "localhost"
unittest_port = 3306
unittest_user = "root"
unittest_password = "123456"
unittest_charset = "UTF8"




