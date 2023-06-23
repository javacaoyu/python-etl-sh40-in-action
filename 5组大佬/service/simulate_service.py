from untils.mysql_util import MySQLUtil
from config import db_config, simulate_log_config as slc
from untils.logging_util import get_logger
from untils import file_util, time_util
from model.simulate_model import Simulate

logger = get_logger()


class SimulateService:
    def __init__(self):
        self.mysql_util = MySQLUtil(
            host=db_config.source_host,
            port=db_config.source_port,
            user=db_config.source_user,
            password=db_config.source_password,
            charset=db_config.source_charset
        )

    def start(self):
        """

        1.读取文件夹下的文件列表，找出以.log结尾的文件
        2.和元数据库中进行对比，找出没有进行采集的文件
        3.读取文件、解析成Model对象、写入到MySQL中
        :return:
        """

        # 1 初始化：创建表
        logger.info("初始化数据库")
        self.mysql_util.check_and_create_table(
            "target",
            slc.simulate_table_name, slc.simulate_table_create_cols_define
        )

        # 2 获要处理的日志文件列表
        need_to_processed_file_list = self.get_need_to_process_file_list()  # 设置了默认值
        print(need_to_processed_file_list)

        # 3 获取要插入的数据
        sql_list = self.get_insert_data_list(need_to_processed_file_list)
        print(len(sql_list))

        # 4写入mysql
        self.write_to_mysql(sql_list)

        # 5 记录已处理文件
        self.record_metadata(need_to_processed_file_list)

        # 6 close
        self.mysql_util.close()

        logger.info(f"【log数据采集】程序运行结束。")

    def write_to_mysql(self, sql_list):
        # 关闭自动提交，走批量执行
        self.mysql_util.disable_autocommit()

        # 提交数据
        try:
            commit_sql_counter = 0
            for item in sql_list:
                self.mysql_util.execute(slc.target_db_name, item)
                commit_sql_counter += 0
            logger.info(
                f"【log数据采集】本次即将向数据库{slc.metadata_db_name}下{slc.simulate_table_name}表提交{commit_sql_counter}条数据，")

        except Exception as e:
            # 处理异常
            self.mysql_util.conn.rollback()
            logger.error(e)
            raise e
        self.mysql_util.conn.commit()
        logger.info("数据已提交成功")

    def get_need_to_process_file_list(
            self,
            files_dir=slc.simulate_log_data_path,
            db=slc.metadata_db_name,
            metadata_table_name=slc.metadata_orders_processed_table_name
    ):
        # 1. 判断元数据表是否存在
        self.mysql_util.check_and_create_table(
            db,
            metadata_table_name,
            db_config.metadata_orders_processed_table_create_cols_define
        )

        # 2. 查询元数据
        processed_list = self.mysql_util.query_result_single_column(
            db,
            f"SELECT `path` FROM {metadata_table_name}"
        )

        # 3. 读取文件列表
        all_files_list = file_util.get_files_list(files_dir, recursion=True)

        # 4. 对比找出需要处理的
        need_to_processed_file_list = file_util.get_new_by_two_list_compare(
            all_files_list,
            processed_list
        )

        return need_to_processed_file_list

    def get_insert_data_list(self, file_list):
        sql_list = []
        for item in file_list:
            with open(item, 'r', encoding="utf-8") as f:
                while True:
                    context = f.readline()
                    if not context:
                        break
                    simulate_data = Simulate(context)
                    sql_list.append(simulate_data.generate_insert_sql())
        return sql_list

    def record_metadata(self, files):
        """
        记录元数据
        :param files: 本次处理的文件列表
        :return: None
        """
        # 确认元数据表存在
        self.mysql_util.check_and_create_table(
            db=db_config.metadata_db_name,
            table_name=db_config.metadata_orders_processed_table_name,
            cols_define=db_config.metadata_orders_processed_table_create_cols_define
        )

        # 执行插入
        self.mysql_util.disable_autocommit()  # 关闭自动提交
        self.mysql_util.conn.begin()  # 开启事务
        try:
            for path in files:
                sql = f"INSERT INTO {db_config.metadata_orders_processed_table_name} VALUES(" \
                      f"NULL, '{path}', '{time_util.get_time()}')"
                self.mysql_util.execute(db_config.metadata_db_name, sql)
        except Exception as e:
            # 如果在企业中，这种类型的错误，可能会直接调用工具代码直接发邮件、或发短信
            logger.critical("元数据记录失败，请立即检查")
            self.mysql_util.conn.rollback()  # 回滚事务
            raise e

        self.mysql_util.conn.commit()  # 提交事务
        logger.info(f"【log数据采集】本次处理的文件：{files}已经处理完成，并完成元数据记录。")
