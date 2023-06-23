# coding:utf8
"""
读取日志的service
"""
from day02.util import mysql_util
from day02.util import time_util
from day02.config import db_config
from day02.util import logger_util
from day02.model.logger_model import *
from day02.config import project_config
from day02.util import file_util

class LoggerService:
    def __init__(self):
        self.logger_csv_path = project_config.csv_output_root_path + \
            "/logger_" + time_util.get_time("%Y-%m-%d_%H_%M_%S") + "csv.tmp"
        self.metadata_mysql_util = mysql_util.MySQLUtil(
            host=metadata_host,
            port=metadata_port,
            user=metadata_user,
            passwd=metadata_passwd,
            charset=metadata_charset
        )
        self.target_mysql_util = mysql_util.MySQLUtil(
            host=target_host,
            port=target_port,
            user=target_user,
            passwd=target_passwd,
            charset=target_charset
        )
        self.logger = logger_util.get_logger()

    def start(self):
        # 1.读取日志文件，返回全部文件的list，读取元数据表，查询已处理过的文件,并和全部文件对比，找出需要处理的文件
        self.logger.info("【获取需要处理的文件】")
        need_file_list = self.get_need_processed_file_list()
        if not need_file_list:
            self.logger.info(f"没有需要处理的文件")
            return None
        self.logger.info(f"采集到需要处理的文件{need_file_list}")
        # 2.组装成logger_model,存到list,返回models_list
        models_list = self.get_models_list(need_file_list)
        # 3.写入到mysql和csv文件中
        self.__write(models_list,need_file_list)
        # 4.写元数据
        # self.record_metadata(need_file_list)


    def get_models_list(self,files):
        models_list = []
        for file in files:
            for line in open(file,'r',encoding='utf8').readlines():
                line = line.strip()
                model = LoggerModel(line)
                models_list.append(model)
        self.logger.info(f"完成转换")
        return models_list


    def get_need_processed_file_list(
            self,
            files_dir=source_logger_path,
            db=metadata_db_name,
            metadata_table_name=metadata_logger_processed_table_name
    ):
        """
        获取需要处理的文件列表
        :param files_dir:
        :param db:
        :param metadata_table_name:
        :return:
        """
        # 1.判断元数据表是否存在
        self.metadata_mysql_util.check_and_create_table(
            db,
            metadata_logger_processed_table_name,
            metadata_logger_processed_table_create_cols_define
        )

        # 2.查询元数据
        processed_list = self.metadata_mysql_util.query_result_single_column(
            db,
            f"select path from {metadata_table_name}"
        )
        self.logger.info(f"读取到元数据记录表{processed_list}")

        # 3.读取文件列表
        all_files_list = file_util.get_file_list(files_dir)      # 记录全部的文件list
        self.logger.info(f"读取到全部文件{all_files_list}")
        # 4.对比找出需要处理的
        need_processed_file_list = file_util.get_new_by_two_list_compare(
            all_files_list,
            processed_list
        )
        self.logger.info(f"需要处理的文件{need_processed_file_list}")

        return need_processed_file_list

    def __write(self, models_list,need_files_list):

        self.target_mysql_util.conn.autocommit(False)       # 关闭自动提交
        self.target_mysql_util.conn.begin()                 # 开启事务
        self.metadata_mysql_util.conn.autocommit(False)     # 关闭自动提交
        self.metadata_mysql_util.conn.begin()               # 开启事务

        try:
            # 1.写出Mysql
            sql_num = self.__write_to_mysql(models_list)
            # self.logger.info(f"{db_config.target_logger_table_name}表插入完成,共插入{sql_num}条数据")
            # 2.写出CSV
            csv_num = self.__write_to_csv(models_list)
            # self.logger.info(f"{self.logger_csv_path}写入完成,共写入{csv_num}条数据")

            # 3.写元数据
            self.record_metadata(need_files_list)
            # self.logger.info(f"【logger数据采集】本次处理文件：{need_files_list}已处理完成，并完成元数据记录")

        except Exception as e:
            # 写日志
            self.target_mysql_util.conn.rollback()
            raise e
        # 提交
        self.target_mysql_util.conn.commit()
        self.logger.info(f"【logger数据采集】本次处理文件：{need_files_list}已处理完成，并完成元数据记录")
        self.metadata_mysql_util.conn.commit()
        self.logger.info(f"{db_config.target_logger_table_name}表插入完成,共插入{sql_num}条数据")

        # csv改名
        file_util.change_file_suffix(self.logger_csv_path, target_suffix="", origin_suffix=".tmp")
        self.logger.info(f"{self.logger_csv_path}写入完成,共写入{csv_num}条数据")

    def __write_to_mysql(self, models_list):
        # 检查写入的目标表是否存在，不存在创建
        self.target_mysql_util.check_and_create_table(
            db_config.target_db_name,
            db_config.target_logger_table_name,
            db_config.target_logger_cols
        )
        counter = 0
        for model in models_list:
            sql = model.generate_insert_sql()
            self.target_mysql_util.execute(db_config.target_db_name, sql)
            counter += 1
        return counter

    def __write_to_csv(self, models_list):
        # open
        csv_write = open(self.logger_csv_path,'w',encoding='utf8')
        # write header
        csv_write.write(LoggerModel.get_csv_header())
        csv_write.write('\n')
        # 写数据
        counter = 0
        for model in models_list:
            csv_write.write(model.to_csv())
            csv_write.write('\n')
            counter += 1
        #close
        csv_write.close()
        return counter

    def record_metadata(self, files):
        try:
            for path in files:
                sql = f"insert into {db_config.metadata_logger_processed_table_name} " \
                      f"values(null,'{path}','{time_util.get_time()}')"
                self.metadata_mysql_util.execute(db_config.metadata_db_name,sql)
        except Exception as e:
            self.logger.critical("【记录元数据失败，请立即检查】")
            self.metadata_mysql_util.conn.rollback()        # 回滚事务
            raise e
        # self.metadata_mysql_util.conn.commit()              # 提交事务
        # self.logger.info(f"【logger数据采集】本次处理文件：{files}已处理完成，并完成元数据记录")


