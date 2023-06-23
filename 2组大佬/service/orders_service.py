# coding:utf8
"""
订单业务服务代码
"""


from day02.util.mysql_util import *
from day02.util.file_util import *
from day02.model.orders_model import *
from day02.config.project_config import *


class OrdersService:
    def __init__(self):
        self.metadata_mysql_util = MySQLUtil(
            host=db_config.metadata_host,
            port=db_config.metadata_port,
            user=db_config.metadata_user,
            passwd=db_config.metadata_passwd,
            charset=db_config.metadata_charset
        )
        self.target_mysql_util = MySQLUtil(
            host=db_config.target_host,
            port=db_config.target_port,
            user=db_config.target_user,
            passwd=db_config.target_passwd,
            charset=db_config.target_charset
        )

        self.logger = logger_util.get_logger()

    def start(self):
        # pass
        # 1.获取处理文件
        self.logger.info("获取需要处理的文件")
        files = self.get_need_processed_file_list()
        if not files:
            self.logger.info(f"没有需要处理的文件")
            return None
        self.logger.info(f"采集到需要处理的文件{files}")
        # print(files)
        # 2.转model对象

        models_list = self.get_models_list(files)
        # 3.转insert sql插入
        # 4.写出csv
        self.__write(models_list)
        # 5.记录元数据
        self.record_metadata()

    def __write(self, models_list):
        # 开启事务
        self.target_mysql_util.conn.begin()

        try:
            # 1.写出Mysql
            self.__write_to_mysql(models_list)
            self.logger.info("数据库插入完成")
            # 2.写出CSV
            self.__write_to_csv(models_list)
            self.logger.info("csv写入完成")
        except Exception as e:
            # 写日志
            self.target_mysql_util.conn.rollback()
            raise e

        # 提交
        self.target_mysql_util.conn.commit()
        # csv改名
        self.__file_remove()

    def get_need_processed_file_list(
            self,
            files_dir=project_config.orders_json_file_data_path,
            db=db_config.metadata_db_name,
            metadata_table_name=db_config.metadata_orders_processed_table_name
    ):
        # 1.判断元数据表是否存在
        self.metadata_mysql_util.check_and_create_table(
            db,
            metadata_table_name,
            db_config.metadata_orders_processed_table_create_cols_define
        )

        # 2.查询元数据
        processed_list = self.metadata_mysql_util.query_result_single_column(
            db,
            f"select path from {metadata_table_name}"
        )
        self.logger.info(f"读取到元数据记录表{processed_list}")

        # 3.读取文件列表
        all_files_list = get_file_list(files_dir)      # 记录全部的文件list
        self.logger.info(f"读取到全部文件{all_files_list}")
        # 4.对比找出需要处理的
        need_processed_file_list = get_new_by_two_list_compare(
            all_files_list,
            processed_list
        )
        self.logger.info(f"需要处理的文件{need_processed_file_list}")

        return need_processed_file_list

    def get_models_list(self, files):
        """
        获取model
        :param files: 文件列表
        :return: model列表
        """
        models_list = []
        for file in files:
            for line in open(file, 'r', encoding='utf8').readlines():
                line = line.strip()
                model = OrdersModel(line)
                models_list.append(model)
        return models_list

    def __write_to_mysql(self, models_list):
        """
        插入数据库
        :param models_list:
        :return:
        """
        self.target_mysql_util.check_and_create_table(
            db_config.target_db_name,
            db_config.target_orders_detail_table_name,
            db_config.target_orders_detail_cols
        )
        self.target_mysql_util.check_and_create_table(
            db_config.target_db_name,
            db_config.target_orders_table_name,
            db_config.target_orders_cols
        )
        # 关闭自动提交
        self.target_mysql_util.conn.autocommit(False)

        orders_detail_count = 0
        for model in models_list:
            self.target_mysql_util.execute(db_config.target_db_name, model.generate_insert_sql())
            for product in model.orders_detail_list:
                self.target_mysql_util.execute(db_config.target_db_name, product.generate_insert_sql())
                orders_detail_count += 1
        self.logger.info(f"即将向{db_config.target_orders_table_name}提交{len(models_list)}条数据，"
                         f"即将向{db_config.target_orders_detail_table_name}提交{orders_detail_count}")

    def __write_to_csv(self, models_list):
        """
        写入csv文件
        :param models_list:
        :return:
        """
        orders_csv_write.write(OrdersModel.get_csv_header()+"\n")
        orders_detail_csv_write.write(OrdersDetailModel.get_csv_header()+"\n")
        csv_orders_detail_count = 0
        for model in models_list:
            orders_csv_line = model.to_csv()
            orders_csv_write.write(orders_csv_line+"\n")
            for product in model.orders_detail_list:
                orders_detail_cvs_line = product.to_csv()
                orders_detail_csv_write.write(orders_detail_cvs_line+"\n")
                csv_orders_detail_count += 1
        self.logger.info(f"即将向{orders_csv_output_path}写入{len(models_list)}条数据，"
                         f"即将向{orders_detail_csv_output_path}写入{csv_orders_detail_count}")

        orders_detail_csv_write.close()
        orders_csv_write.close()

    def __file_remove(self):
        pass

    def record_metadata(self):
        # 检查是否存在
        self.metadata_mysql_util.check_and_create_table(
            db_config.metadata_db_name,
            db_config.metadata_orders_processed_table_name,
            db_config.metadata_orders_processed_table_create_cols_define
        )
        # 关闭自动提交
        self.metadata_mysql_util.conn.autocommit(False)

        try:
            files_list = self.get_need_processed_file_list()
            for file in files_list:
                # 插入数据
                self.metadata_mysql_util.execute_force_commit(
                    db_config.metadata_db_name,
                    f"insert into {db_config.metadata_orders_processed_table_name} values(null,'{file}','{time_util.get_today()}')"
                )
        except Exception as e:
            self.logger.critical("元数据记录失败，清理立即检查")
            self.metadata_mysql_util.conn.rollback()
            raise e


