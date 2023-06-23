# coding:utf8
"""
订单的业务服务代码

完成数据采集 -> MYSQL
订单服务类映射的就是：采集数据采集 -> MYSQL
"""
from util.mysql_util import MySQLutil
from config import db_config
from util.file_util import *
from model.orders_model import OrdersDetailModel, OrdersModel
from util import time_util


class OrdersService:
    def __init__(self):
        self.metadata_mysql_util = MySQLutil(
            host=db_config.metadata_host,
            port=db_config.metadata_port,
            user=db_config.metadata_user,
            password=db_config.metadata_password
        )
        self.target_mysql_util = MySQLutil(
            host=db_config.target_host,
            port=db_config.target_port,
            user=db_config.target_user,
            password=db_config.target_password
        )


    def start(self):
        # 1,获取需要处理的文件
        files: list = self.get_need_to_process_file_list()
        # 2，转model对象
        model_list = self.get_models_list(files)

        # 开启事务
        self.target_mysql_util.conn.begin()
        try:
            # 3，转insert sql写入
            self.write(model_list)
            # 4，写出csv
            # 5，记录元数据

        except Exception as e:
            self.target_mysql_util.conn.rollback()  # 出现错误就回滚
            raise e



    def write(self, models_list):
        self.__write_to_mysql(models_list)
        self.__write_to_csv(models_list)

    def __write_to_csv(self,models_list):
        # 订单表和订单详情表的存储路径
        orders_csv_path = project_config.csv_output_root_path+'/orders_'+\
                          time_util.get_time('%Y%m%d_%H%M%S')+'.csv.tmp'
        orders_detail_csv_path = project_config.csv_output_root_path+'/orders_detail_'+\
                                 time_util.get_time('%Y%m%d_%H%M%S')+'.csv.tmp'
        # 对象
        orders_csv_write = open(orders_csv_path,'w',encoding="UTF-8")
        orders_detail_csv_write = open(orders_detail_csv_path,'w',encoding="UTF-8")
        # 调用类的静态方法写标头
        orders_csv_write.write(OrdersModel.get_csv_header())
        orders_csv_write.write('\n')
        orders_detail_csv_write.write(OrdersDetailModel.get_csv_header())
        orders_detail_csv_write.write('\n')
        for model in models_list:
            orders_csv_write.write(model.to_csv())
            orders_csv_write.write('\n')
            for i in model.order_detail_model_list():
                orders_detail_csv_write.write(i.to_csv())
                orders_detail_csv_write.write('\n')

        orders_csv_write.close()
        orders_detail_csv_write.close()



    def __write_to_mysql(self,models_list):
        """

        :return:
        """
        # 检查表是否存在，不存在则创建
        self.target_mysql_util.check_table_and_create(
            db_config.target_db_name,db_config.target_orders_table_name,db_config.target_orders_cols)
        self.target_mysql_util.check_table_and_create(
            db_config.target_db_name,db_config.target_orders_detail_table_name,db_config.target_order_detail_cols)
        # 关闭自动提交
        self.target_mysql_util.close_autocommit()


        for model in models_list:
            sql = model.generate_insert_sql()   # 订单表插入语句
            self.target_mysql_util.execute(db_config.target_db_name,sql)
            #  todo 没看懂
            for i in model.order_detail_model_list:
                sql = i.generate_insert_sql()
                self.target_mysql_util.execute(db_config.target_db_name,sql)


    def get_need_to_process_file_list(self,
        files_dir = project_config.orders_json_file_data_path,
        db = db_config.metadata_db_name,
        metadata_table_name = db_config.metadata_orders_processed_table_name):
        # 1. 判断元数据表是否存在
        self.metadata_mysql_util.check_table_and_create(db,metadata_table_name,db_config.metadata_table_columns)

        #
        # 2. 查询元数据
        process_list = self.metadata_mysql_util.query_result_single_column(db,
                                    f"select path from {metadata_table_name}")

        # 3. 读取文件列表
        all_file_list = get_all_file_list(files_dir,recursion=True)
        # 4，对比找出需要处理的
        need_to_processed_file_list = get_new_by_two_list_compera(all_file_list,process_list)

        return need_to_processed_file_list

    def get_models_list(self,files):
        """
        读取文件，转换成订单模型，封装到list内
        :param files: list记录文件路径
        :return: list（内函OrdersModel对象）
        """
        models_list = []
        for path in files:
            for line in open(path,'r',encoding='UTF-8').readlines():
                line = line.strip()
                model = OrdersModel(line)
                models_list.append(model)
        return models_list

