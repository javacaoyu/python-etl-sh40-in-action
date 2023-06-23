"""
订单业务服务代码
"""
import os

from util.mysql_util import MySQLUtil
from util import str_util, file_unit, time_util, logging_util
from config import db_config, project_config
from model.orders_model import OrdersModel, OrdersDetailModel

class OrdersService:

    def __init__(self):
        self.metadata_mysql_util = MySQLUtil(
            host=db_config.metadata_host,
            port=db_config.metadata_port,
            user=db_config.metadata_user,
            password=db_config.metadata_password,
            charset=db_config.metadata_charset
        )
        self.target_mysql_util = MySQLUtil(
            host=db_config.target_host,
            port=db_config.target_port,
            user=db_config.target_user,
            password=db_config.target_password,
            charset=db_config.target_charset
        )
        self.logger = logging_util.get_logger()
        self.orders_csv_path = project_config.csv_output_root_path + "/orders_" + time_util.get_time(
            "%Y-%m-%d_%H_%M_%S") + ".csv.tmp"
        self.orders_detail_csv_path = project_config.csv_output_root_path + "/orders_datail_" + time_util.get_time(
            "%Y-%m-%d_%H_%M_%S") + ".csv.tmp"

    def start(self):
        # todo 1获取需要处理的文件
        files: list = self.get_need_to_process_file_list()
        if not files:
            self.logger.warning("本次无文件需要处理，程序退出")
            return None
        self.logger.info(f"本次需要处理文件{files}")
        # todo 2转model对象
        models_list: list = self.get_models_list(files)
        # todo 3写出mysql和csv
        self.write(models_list)
        # todo 4记录元数据
        self.record_metadata(files)
        # todo 5结束
        self.metadata_mysql_util.close()
        self.target_mysql_util.close()

    def get_need_to_process_file_list(
            self,
            files_dir=project_config.orders_json_file_data_path,
            db=db_config.metadata_db_name,
            metadata_table_name=db_config.metadata_processed_table_name
    ):
        """
        获取需要处理的文件
        :param files_dir: json文件路径
        :param db: 元数据库
        :param metadata_table_name: 与数据表名
        :return: 需要处理文件绝对路径列表
        """
        # 1。判断元数据是否存在
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

        # 3。读取文件列表
        all_files_list = []
        all_files_list = file_unit.get_files_list(files_dir, recursion=True)
        # for name in os.listdir(files_dir):
        #     file_absolute_path = files_dir + "/" + name
        #     all_files_list.append(str_util.unite_path_slash(file_absolute_path))

        # 4.对比找出需要处理的
        need_to_processed_file_list = file_unit.get_new_by_two_list_compare(
            all_files_list,
            processed_list
        )
        return need_to_processed_file_list

    def get_models_list(self, files):
        """
        读取文件，转换为订单模型，封装到list内
        :param files: 文件绝对路径列表
        :return: 订单模型列表
        """
        orders_model_list = []
        for file in files:
            for line in open(file, 'r', encoding='utf8').readlines():
                line = line.strip()
                order = OrdersModel(line)
                orders_model_list.append(order)
        return orders_model_list

    def write(self, models_list):
        """
        写出MySQL和csv
        :param models_list:
        :return:
        """
        # 开启事务
        self.target_mysql_util.conn.begin()
        # 1.写出到MySQL
        # 2.写出到csv(写出文件名是xxx.csv.tmp),如果MySQL  OK .tmp后缀删除
        try:
            self.__write_to_mysql(models_list)
            self.__write_to_csv(models_list)
        except Exception as e:
            # 写出异常，数据库回滚，csv文件不改名
            self.target_mysql_util.conn.rollback()
            raise e
        # 写出成功，MySQL提交事务，csv改名
        self.target_mysql_util.conn.commit()
        file_unit.change_file_suffix(self.orders_csv_path, "", '.tmp')
        file_unit.change_file_suffix(self.orders_detail_csv_path, "", '.tmp')

    def __write_to_mysql(self, models_list):
        """
        将模型list的内容，写出到MySQL数据库（订单表、订单详情表）
        :param models_list:
        :return:
        """
        # 如果目标表orders不存在，提前创建
        self.target_mysql_util.check_and_create_table(
            db=db_config.target_db_name,
            table_name=db_config.target_orders_table_name,
            cols_define=db_config.target_orders_processed_table_create_cols_define
        )
        # 如果目标表orders_detail不存在，提前创建
        self.target_mysql_util.check_and_create_table(
            db=db_config.target_db_name,
            table_name=db_config.target_orders_detail_table_name,
            cols_define=db_config.target_orders_detail_processed_table_create_cols_define
        )
        # 关闭自动提交，走批量
        self.target_mysql_util.disable_autocommit()
        orders_nums = 0
        orders_detail_nums = 0
        for model in models_list:
            sql = model.generate_insert_sql()  # 订单表的插入语句
            self.target_mysql_util.execute(db_config.target_db_name, sql)
            orders_nums += 1
            for datail_model in model.orders_detail_model_list:
                sql = datail_model.generate_insert_sql()
                self.target_mysql_util.execute(db_config.target_db_name, sql)
                orders_detail_nums += 1
        self.logger.info(f"本次mysql插入orders数据{orders_nums}")
        self.logger.info(f"本次mysql插入orders_detail数据{orders_detail_nums}")
    def __write_to_csv(self, models_list):

        # 获取写文件的对象
        orders_csv_writer = open(self.orders_csv_path, 'w', encoding="utf8")
        orders_detail_csv_writer = open(self.orders_detail_csv_path, 'w', encoding="utf8")

        # 写出csv标头
        orders_csv_writer.write(OrdersModel.get_csv_header())
        orders_csv_writer.write("\n")
        orders_detail_csv_writer.write(OrdersDetailModel.get_csv_header())
        orders_detail_csv_writer.write("\n")
        orders_nums = 0
        orders_detail_nums = 0
        for model in models_list:
            csv_line = model.to_csv()
            orders_csv_writer.write(csv_line)
            orders_csv_writer.write("\n")
            orders_nums += 1
            for detail_model in model.orders_detail_model_list:
                csv_line = detail_model.to_csv()
                orders_detail_csv_writer.write(csv_line)
                orders_detail_csv_writer.write("\n")
                orders_detail_nums += 1
        self.logger.info(f"本次csv插入orders数据{orders_nums}")
        self.logger.info(f"本次csv插入orders_detail数据{orders_detail_nums}")

    def record_metadata(self, files):
        """
        记录元数据
        :param files: 要记录的元数据
        :return: None
        """
        # 确认元数据表是否存在
        self.metadata_mysql_util.check_and_create_table(
            db=db_config.metadata_db_name,
            table_name=db_config.metadata_processed_table_name,
            cols_define=db_config.metadata_orders_processed_table_create_cols_define
        )

        # 执行插入
        self.metadata_mysql_util.disable_autocommit()
        self.metadata_mysql_util.conn.begin()
        try:
            for path in files:
                sql = f"insert into {db_config.metadata_processed_table_name} values(" \
                      f"null, '{path}', '{time_util.get_time()}')"
                self.metadata_mysql_util.execute(db_config.metadata_db_name, sql)
        except Exception as e:
            self.logger.critical("写入元数据错误，请检查")
            self.metadata_mysql_util.conn.rollback()
            raise e
        self.metadata_mysql_util.conn.commit()
        self.logger.info(f"写入元数据{files}")
