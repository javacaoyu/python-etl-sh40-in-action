from util.mysql_util import MySQLutil
from config import db_config, project_config
from util import file_util, str_util, time_util, logging_util
from model.logs_model import LogModel


class BackendLogsService:
    def __init__(self):
        # 元数据记录表
        # 数据导出mysql表
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
        self.logger = logging_util.get_logger()
        self.logs_output_csv_path = str_util.unite_path_slash(
            project_config.log_output_csv_path+'/logs_'+time_util.get_time("%Y%m%d_%H%M%S")+".csv.tmp")


    def start(self):
        # 1. 读取元数据记录，找出已处理的
        # 2. 读取数据文件夹，找出全部文件
        # 3. 对比，找出本次要处理的
        need_to_handle_list = self.get_need_to_handle_list()
        if not need_to_handle_list:
            self.logger.info(f"【日志信息采集】本次无文件需要处理，程序退出")
            return None
        self.logger.info(f"【日志信息采集】本次需要采集的文件是：{need_to_handle_list}，文件条数：{len(need_to_handle_list)}")
        # 4. 读取数据、转换为Model对象
        model_list = self.get_model_list()
        # 5. 将model对象
        #    1. 写出MySQL
        #    2. 写出CSV
        self.__write(model_list)
        # 6. 记录元数据
        self.record_metadata(need_to_handle_list)
        # 7. 结束
        self.metadata_mysql_util.close()
        self.target_mysql_util.close()

        self.logger.info(f"【日志信息采集】程序运行结束。")


    def record_metadata(self, files):
        # 开启事务
        self.metadata_mysql_util.conn.begin()
        try:
            for i in files:
                sql = f"insert into {db_config.metadata_logs_table_name} values (" \
                      f"null,'{i}','{time_util.get_time()}')"
                self.metadata_mysql_util.execute(db_config.metadata_db_name, sql)
        except Exception as e:
            self.metadata_mysql_util.conn.rollback()
            raise e

        # 提交事务
        self.metadata_mysql_util.conn.commit()

    def __write(self, model_list):
        # 开启事务
        self.target_mysql_util.conn.begin()
        try:
            #    1. 写出MySQL
            self.__write_to_sql(model_list)
            #    2. 写出CSV
            self.__write_to_csv(model_list)
        except Exception as e:
            self.target_mysql_util.conn.rollback()
            raise e
        # 提交事务
        self.target_mysql_util.conn.commit()

        # 更改后缀
        file_util.change_file_suffix(self.logs_output_csv_path, "", ".tmp")


    def __write_to_sql(self, model_list):
        self.target_mysql_util.check_table_and_create(
            db_config.target_db_name,
            db_config.target_logs_table_name,
            db_config.target_logs_table_create_sql)
        for model in model_list:
            sql = model.generate_insert_sql(db_config.target_logs_table_name)
            self.target_mysql_util.execute(db_config.target_db_name, sql)


    def __write_to_csv(self, model_list):
        with open(self.logs_output_csv_path, 'w', encoding="UTF-8") as f:
            f.write(LogModel.to_csv_header())
            f.write('\n')
            for model in model_list:
                line = model.to_csv()
                f.write(line)
                f.write('\n')

    def get_need_to_handle_list(self):
        """
        对比全部数据列表和元数据列表，找出需要处理的列表
        :return: list
        """
        # 1. 读取元数据记录，找出已处理的
        metadata_list = self.get_metadata_list()
        # 2. 读取数据文件夹，找出全部文件
        all_file_list = self.get_all_files_list()
        list1 = file_util.get_new_by_two_list_compera(all_file_list, metadata_list)
        return list1

    def get_metadata_list(self):
        self.metadata_mysql_util.check_table_and_create(
            db_config.metadata_db_name,
            db_config.metadata_logs_table_name,
            db_config.metadata_logs_table_create_sql)
        list1 = self.metadata_mysql_util.query_result_single_column(
            db_config.metadata_db_name,
            f"select path from {db_config.metadata_logs_table_name}"
        )
        return list1

    @staticmethod
    def get_all_files_list():
        list1 = file_util.get_all_file_list(path=project_config.log_from_path, recursion=True)
        return list1

    @staticmethod
    def get_model_list():
        model_list = []
        for i in file_util.get_file_content(project_config.log_from_path):
            model = LogModel(i)
            model_list.append(model)
        return model_list
