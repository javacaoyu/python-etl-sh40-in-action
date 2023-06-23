"""
日志服务
"""
import sys

from util.mysql_util import MySQLUtil
from util import logging_util, file_unit, time_util
from config import db_config, project_config
from model.backend_model import BackendModel

class BackendService(object):
    def __init__(self):
        """
        日志文件信息采集服务
        """
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
        # 日志的CSV文件绝对路径
        self.backend_csv_path = project_config.backend_csv_output_root_path + '/' + time_util.get_time("%Y-%m-%d_%H_%M_%S") + ".csv.tmp"

    def start(self):
        # todo 获取需要处理的文件
        files: list = self.get_need_to_process_file_list()
        if not files:
            self.logger.info("本次操作没有要处理的文件，程序退出")
            sys.exit(0)

        # todo 转model对象
        model_list: list = self.get_model_list(files)

        # todo 写出mysql和csv
        self.write(model_list)

        # todo 写出元数据
        self.record_metadata(files)

        # todo 结束
        self.metadata_mysql_util.close()
        self.target_mysql_util.close()

    def get_need_to_process_file_list(self) -> list:
        """
        获取需要处理的文件列表
        :return: list
        """
        # 1.获取已处理过的文件列表
        # 1.1 元数据表是否已存在，未存在需创建
        self.metadata_mysql_util.check_and_create_table(
            db=db_config.metadata_db_name,
            table_name=db_config.metadata_backend_processed_table_name,
            cols_define=db_config.metadata_backend_processed_table_create_cols_define
        )
        # 1.2 获取已处理过的文件列表
        processed_file_list = self.metadata_mysql_util.query_result_single_column(
            db=db_config.metadata_db_name,
            sql=f"select path from {db_config.metadata_backend_processed_table_name}"
        )

        # 2.获取路径下的全部文件列表
        all_files_list = file_unit.get_files_list(
            project_config.backend_file_data_path,
            recursion=True
        )

        # 3.对比获得需要采集的文件信息
        need_to_processed_lists = file_unit.get_new_by_two_list_compare(all_files_list, processed_file_list)

        self.logger.info(f"本次需要处理的文件有{need_to_processed_lists}")

        return need_to_processed_lists

    def get_model_list(self, files) -> list:
        """
        根据文件列表的路径读出文件中的每行数据，将数据转为BackendModel对象
        :param files: 文件列表
        :return: 元素为BackendModel对象的列表
        """
        model_list = list()
        for file in files:
            for line in open(file, 'r', encoding='utf8').readlines():
                line = line.strip()
                model = BackendModel(line)
                model_list.append(model)

        return model_list

    def write(self, model_list):
        """
        写出数据到MySQL和CSV
        :param model_list: 元素为BackendModel对象的列表
        :return: None
        """
        # 1开启事务并关闭自动提交
        self.target_mysql_util.conn.begin()
        self.target_mysql_util.conn.autocommit(False)
        try:
            # 写出到MySQL
            self.__write_to_mysql(model_list)
            # 写出到csv
            self.__write_to_csv(model_list)
        except Exception as e:
            # 写入失败，MySQL数据回滚
            self.target_mysql_util.conn.rollback()
            raise e
        # 写入MySQL成功，事务提交处理
        self.target_mysql_util.conn.commit()
        # 写入csv成功，文件改名
        file_unit.change_file_suffix(self.backend_csv_path, "", ".tmp")

    def __write_to_mysql(self, model_list):
        """
        写出数据到MySQL
        :param model_list: 元素为BackendModel对象的列表
        :return: None
        """
        # 1.检查目标表是否存在，不存在创建
        self.target_mysql_util.check_and_create_table(
            db=db_config.target_db_name,
            table_name=db_config.target_backend_table_name,
            cols_define=db_config.target_backend_processed_table_create_cols_define
        )
        # 2.目标表存在，开启事务，关闭自动提交
        self.target_mysql_util.conn.begin()
        self.target_mysql_util.conn.autocommit(False)

        backend_nums = 0
        for model in model_list:
            backend_nums += 1
            sql = model.generate_insert_sql(db_config.target_backend_table_name)
            self.target_mysql_util.execute(db_config.target_db_name, sql)
        self.logger.info(f"本次执行向MySQL插入{backend_nums}条数据")

    def __write_to_csv(self, model_list):
        """
        写出数据到CSV
        :param model_list: 元素为BackendModel对象的列表
        :return: None
        """
        # 1.写csv标头
        backend_writer = open(self.backend_csv_path, 'w', encoding='utf8')
        backend_writer.write(BackendModel.get_csv_header())
        backend_writer.write('\n')
        # 2.写数据
        backend_nums = 0
        for model in model_list:
            backend_nums += 1
            csv_line = model.to_csv()
            backend_writer.write(csv_line)
            backend_writer.write('\n')
        self.logger.info(f"本次执行向CSV插入{backend_nums}条数据")

    def record_metadata(self, files):
        """
        将此次处理过的文件路径记录到元数据库
        :param files: 此次处理的文件列表
        :return: None
        """
        # 1 元数据表是否已存在，未存在需创建
        self.metadata_mysql_util.check_and_create_table(
            db=db_config.metadata_db_name,
            table_name=db_config.metadata_backend_processed_table_name,
            cols_define=db_config.metadata_backend_processed_table_create_cols_define
        )
        # 开启事务,关闭自动提交
        self.metadata_mysql_util.conn.begin()
        self.metadata_mysql_util.conn.autocommit(False)
        try:
            for file in files:
                self.metadata_mysql_util.execute(
                    db=db_config.metadata_db_name,
                    sql=f"insert into {db_config.metadata_backend_processed_table_name} values ("
                        f"NULL,"
                        f"'{file}',"
                        f"'{time_util.get_time()}'"
                        f")"
                )
        except Exception as e:
            self.logger.critical("写入元数据错误，请检查")
            self.metadata_mysql_util.conn.rollback()
            raise e
        self.metadata_mysql_util.conn.commit()
        self.logger.info(f"已写入元数据{files}")
