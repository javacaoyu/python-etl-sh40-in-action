import sys
from config import db_config, project_config, logging_config
from util import mysql_util, logging_util, file_util, time_util
from model import backend_data_model


class BackendDataService:
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
        self.logger = logging_util.get_logger(log_path=logging_config.backend_data_default_logger_file_full_path)
        self.backend_data_csv_path = f"{project_config.csv_output_root_path}" \
                                     f"\\backend_data_{time_util.get_time('%Y%m%d_%H%M%S')}.csv.tmp"

    def start(self):
        # 1. 获取需要处理的文件
        files = self.get_need_to_process_file_list()
        if not files:
            self.logger.info(f"{project_config.backend_data_path}目录暂无更新文件，无需处理文件。")
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
            files_dir=project_config.backend_data_path,
            db=db_config.metadata_db_name,
            metadata_table_name=db_config.metadata_processed_table_name
    ):
        if self.metadata_mysql.check_and_create_table(
                db=db,
                table_name=metadata_table_name,
                cols_define=db_config.metadata_orders_processed_table_create_cols_define
        ):
            self.logger.info(f"元数据表{metadata_table_name}不存在，现已创建")
        processed_list = self.metadata_mysql.query_result_single_column(db, f"select path from {metadata_table_name}")
        all_files_list = file_util.get_files_list(files_dir, recursion=True)
        need_to_processed_file_list = file_util.get_new_by_two_list_compare(all_files_list, processed_list)
        return need_to_processed_file_list

    @staticmethod
    def get_models_list(files):
        models_list = []
        for path in files:
            for line in open(path, 'r', encoding='utf8').readlines():
                line = line.strip()
                model = backend_data_model.BackendDataModel(line)
                models_list.append(model)
        return models_list

    def __write_to_mysql(self, models_list):
        # 如果表不存在，提前创建
        self.target_mysql.check_and_create_table(
            db=db_config.target_db_name,
            table_name=db_config.target_backend_data_table_name,
            cols_define=db_config.target_backend_data_table_cols_define
        )
        self.target_mysql.disable_autocommit()  # 关闭自动提交事务
        for model in models_list:
            sql = model.generate_insert_sql()
            self.target_mysql.execute(db_config.target_db_name, sql)
        self.logger.info(f"共向{db_config.target_backend_data_table_name}表插入{len(models_list)}条数据。")

    def __write_to_csv(self, models_list):
        # 获取写入文件对象
        backend_data_csv_writer = open(self.backend_data_csv_path, 'w', encoding='utf8')
        # 写入标头
        backend_data_csv_writer.write(backend_data_model.BackendDataModel.get_csv_header())
        backend_data_csv_writer.write("\n")
        # 写入数据
        for model in models_list:
            csv_line = model.to_csv()
            backend_data_csv_writer.write(csv_line)
            backend_data_csv_writer.write("\n")
        backend_data_csv_writer.close()
        self.logger.info(f"共向{project_config.csv_output_root_path}文件插入{len(models_list)}条数据。")

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
        file_util.change_file_suffix(self.backend_data_csv_path, target_suffix="", origin_suffix=".tmp")

    def record_metadata(self, files):
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
