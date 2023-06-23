# coding:utf8
"""
订单的业务服务代码

完成数据采集 -> MYSQL
订单服务类映射的就是：采集数据采集 -> MYSQL
"""
import sys

from config import db_config, project_config
from model import orders_model, orders_detail_model
from util import mysql_util, file_util, time_util, logging_util


class OrdersService:
    def __init__(self):
        self.metadata_mysql = mysql_util.MysqlUtil(
            host=db_config.metadata_host,
            port=db_config.metadata_port,
            user=db_config.metadata_user,
            password=db_config.metadata_password,
            charset=db_config.metadata_charset
        )
        self.target_mysql = mysql_util.MysqlUtil(
            host=db_config.target_host,
            port=db_config.target_port,
            user=db_config.target_user,
            password=db_config.target_password,
            charset=db_config.target_charset
        )
        self.logger = logging_util.get_logger()
        self.orders_csv_path = f"{project_config.csv_output_root_path}\\orders_{time_util.get_time('%Y%m%d_%H%M%S')}.csv.tmp"
        self.orders_detail_csv_path = f"{project_config.csv_output_root_path}\\orders_detail_{time_util.get_time('%Y%m%d_%H%M%S')}.csv.tmp"

    def start(self):
        # 1. 获取需要处理的文件
        files: list = self.get_need_to_process_file_list()
        if not files:
            self.logger.info(f"{project_config.orders_json_file_data_path}目录暂无更新文件，无需处理文件。")
            sys.exit()
        else:
            self.logger.info(f"本次需要采集的文件为{files}，共{len(files)}个文件")
        # 2. 转model对象
        models_list = self.get_models_list(files)
        # 3. 写出（包含MySQL写出和CSV写出）
        self.__write(models_list)
        # 4. 记录元数据
        self.record_metadata(files)
        # 5. 关闭数据库对象
        self.metadata_mysql.close()
        self.target_mysql.close()

    def get_need_to_process_file_list(
            self,
            files_dir=project_config.orders_json_file_data_path,
            db=db_config.metadata_db_name,
            metadata_table_name=db_config.metadata_processed_table_name
    ):
        # 判断元数据表事否存在，不存在创建
        if self.metadata_mysql.check_and_create_table(
            db=db,
            table_name=metadata_table_name,
            cols_define=db_config.metadata_orders_processed_table_create_cols_define
        ):
            self.logger.info(f"元数据表{metadata_table_name}不存在，现已创建")
        # 查询元数据表中已处理的文件目录
        processed_list = self.metadata_mysql.query_result_single_column(db, f'select path from {metadata_table_name}')
        # 读取文件列表
        all_files_list = file_util.get_files_list(files_dir, recursion=True)
        need_to_processed_file_list = file_util.get_new_by_two_list_compare(all_files_list, processed_list)
        return need_to_processed_file_list

    @staticmethod
    def get_models_list(files):
        """
        读取文件，转换成订单模型，封装到list内
        :param files: list记录文件路径
        :return: list（内函OrdersModel对象）
        """
        models_list = []
        for path in files:
            for line in open(path, 'r', encoding='utf8').readlines():
                line = line.strip()
                model = orders_model.OrdersModel(line)
                models_list.append(model)
        return models_list

    def __write_to_mysql(self, models_list):
        """
        将模型list的内容，写入MySQL数据库(订单表和订单详情表）
        :return: None
        """
        # 如果订单表不存在，提前创建
        self.target_mysql.check_and_create_table(
            db=db_config.target_db_name,
            table_name=db_config.target_orders_table_name,
            cols_define=db_config.target_orders_table_cols_define
        )
        # 如果订单详情表不存在，提前创建
        self.target_mysql.check_and_create_table(
            db=db_config.target_db_name,
            table_name=db_config.target_orders_detail_table_name,
            cols_define=db_config.target_orders_detail_table_cols_define
        )
        self.target_mysql.disable_autocommit()  # 关闭自动提交事务
        flg1 = 0
        for model in models_list:
            sql = model.generate_insert_sql()
            self.target_mysql.execute(db_config.target_db_name, sql)
            for detail_model in model.orders_detail_model_list:
                flg1 += 1
                sql = detail_model.generate_insert_sql()
                self.target_mysql.execute(db_config.target_db_name, sql)
        self.logger.info(f"共向{self.orders_csv_path}表插入{len(models_list)}条数据。\n"
                         f"共向{self.orders_detail_csv_path}表插入{flg1}条数据")

    def __write_to_csv(self, models_list):
        """
        将模型list的内容，写入csv文件(订单表和订单详情表）
        :return:
        """
        # 获取写入文件对象
        orders_csv_writer = open(self.orders_csv_path, 'w', encoding='utf8')
        orders_detail_csv_writer = open(self.orders_detail_csv_path, 'w', encoding='utf8')
        # 写入标头
        orders_csv_writer.write(orders_model.OrdersModel.get_csv_header())
        orders_csv_writer.write("\n")
        orders_detail_csv_writer.write(orders_detail_model.OrdersDetailModel.get_csv_header())
        orders_detail_csv_writer.write("\n")

        # 写入数据
        flg2 = 0
        for model in models_list:
            csv_line = model.to_csv()
            orders_csv_writer.write(csv_line)
            orders_csv_writer.write("\n")
            for detail_model in model.orders_detail_model_list:
                flg2 += 1
                csv_line = detail_model.to_csv()
                orders_detail_csv_writer.write(csv_line)
                orders_detail_csv_writer.write("\n")
        orders_csv_writer.close()
        orders_detail_csv_writer.close()
        self.logger.info(f"共向{project_config.csv_output_root_path}文件插入{len(models_list)}条数据。\n"
                         f"共向{db_config.target_orders_detail_table_name}文件插入{flg2}条数据")

    def __write(self, models_list):
        # 1. to mysql
        # 开启事务
        self.target_mysql.conn.begin()  # 开启事务
        try:
            self.__write_to_mysql(models_list)
            self.__write_to_csv(models_list)
        except Exception as e:
            # 如果有异常，mysql回退，csv不改名
            self.target_mysql.conn.rollback()  # 回滚
            raise e

        # 没有异常
        # mysql 提交
        self.target_mysql.conn.commit()
        # csv改名
        file_util.change_file_suffix(self.orders_csv_path, target_suffix="", origin_suffix=".tmp")
        file_util.change_file_suffix(self.orders_detail_csv_path, target_suffix="", origin_suffix=".tmp")

    def record_metadata(self, files):
        """
        记录元数据
        :param files: 本次处理的文件列表
        :return: None
        """
        # 确认元数据表存在
        if self.metadata_mysql.check_and_create_table(
            db=db_config.metadata_db_name,
            table_name=db_config.metadata_processed_table_name,
            cols_define=db_config.metadata_orders_processed_table_create_cols_define
        ):
            self.logger.info(f"元数据表{db_config.metadata_processed_table_name}不存在，现已创建")
        # 执行插入
        self.metadata_mysql.disable_autocommit()  # 关闭事务
        self.metadata_mysql.conn.begin()  # 开启事务
        try:
            for path in files:
                sql = f"insert into {db_config.metadata_processed_table_name}(" \
                      f"id, path, processed_date) values(" \
                      f"null, '{path}', '{time_util.get_time()}')"
                self.metadata_mysql.execute(db_config.metadata_db_name, sql)
        except Exception as e:
            self.logger.critical("元数据记录失败，请立即查看！")
            self.metadata_mysql.conn.rollback()
            raise e
        self.metadata_mysql.conn.commit()
        self.logger.info(f"共向元数据插入{len(files)}条数据")



