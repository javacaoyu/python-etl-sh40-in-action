"""
模拟日志相关的配置项
"""
simulate_log_data_path = "./simulate_data"  # 模拟日志源文件目录
simulate_table_name = "simulate"
metadata_db_name = "metadata"
target_db_name = "target"
metadata_orders_processed_table_name = "orders_processed_files"
simulate_table_create_cols_define = """
`id`        INT   auto_increment primary key,
`date`      VARCHAR(255) COMMENT '日志时间',
`level`     VARCHAR(255) COMMENT '日志等级',
`file`      VARCHAR(255) COMMENT '文件名',
`time`      INT COMMENT '耗时',
`province`  VARCHAR(255) COMMENT '省份',
`region`    VARCHAR(255) COMMENT '市',
`data`      VARCHAR(255) COMMENT '数据'
"""
