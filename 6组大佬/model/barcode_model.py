"""
商品（条码信息）模型
"""
from config import project_config, db_config


class BarcodeModel:

    def __init__(self, data_tuple=None):
        """
        Note:data_tuple是传入的数据元组，请确保元组内流顺序遵循如下顺序：
        - code
        - name
        - spec
        - trademark
        - addr
        - units
        - factory_name
        - trade_price
        - retail_price
        - update_at
        - wholeunit
        - wholenum
        - img
        - src
        :param data_tuple:
        """
        self.code = data_tuple[0]
        self.name = data_tuple[1]
        self.spec = data_tuple[2]
        self.trademark = data_tuple[3]
        self.addr = data_tuple[4]
        self.units = data_tuple[5]
        self.factory_name = data_tuple[6]
        self.trade_price = data_tuple[7]
        self.retail_price = data_tuple[8]
        self.updateAt = data_tuple[9]
        self.wholeunit = data_tuple[10]
        self.wholenum = data_tuple[11]
        self.img = data_tuple[12]
        self.src = data_tuple[13]

    def generate_insert_sql(
            self,
            table_name=db_config.metadata_barcode_processed_table_name
    ):
        sql = f"insert into {table_name}(code,name,spec,trademark,addr," \
              f"units,factory_name,trade_price,retail_price,updateAt," \
              f"wholeunit,wholenum,img,src) values(" \
              f"'{self.code}'," \
              f"'{self.name}'," \
              f"'{self.spec}'," \
              f"'{self.trademark}'," \
              f"'{self.addr}'," \
              f"'{self.units}'," \
              f"'{self.factory_name}'," \
              f"'{self.trade_price}'," \
              f"'{self.retail_price}'," \
              f"'{self.updateAt}'," \
              f"'{self.wholeunit}'," \
              f"{self.wholenum}," \
              f"'{self.img}'," \
              f"'{self.src}'" \
              f")"
        return sql

    @staticmethod
    def get_csv_header():
        csv_header = f"code{project_config.csv_output_sep}" \
                     f"name{project_config.csv_output_sep}" \
                     f"spec{project_config.csv_output_sep}" \
                     f"trademark{project_config.csv_output_sep}" \
                     f"addrunits{project_config.csv_output_sep}," \
                     f"factory_name{project_config.csv_output_sep}" \
                     f"trade_price{project_config.csv_output_sep}" \
                     f"retail_price{project_config.csv_output_sep}" \
                     f"updateAt{project_config.csv_output_sep}" \
                     f"wholeunit{project_config.csv_output_sep}" \
                     f"wholenum{project_config.csv_output_sep}" \
                     f"img{project_config.csv_output_sep}" \
                     f"src"
        return csv_header

    def to_csv(self):
        csv_line = f"{self.code}{project_config.csv_output_sep}" \
                   f"{self.name}{project_config.csv_output_sep}" \
                   f"{self.spec}{project_config.csv_output_sep}" \
                   f"{self.trademark}{project_config.csv_output_sep}" \
                   f"{self.addr}{project_config.csv_output_sep}" \
                   f"{self.units}{project_config.csv_output_sep}" \
                   f"{self.factory_name}{project_config.csv_output_sep}" \
                   f"{self.trade_price}{project_config.csv_output_sep}" \
                   f"{self.retail_price}{project_config.csv_output_sep}" \
                   f"{self.updateAt}{project_config.csv_output_sep}" \
                   f"{self.wholeunit}{project_config.csv_output_sep}" \
                   f"{self.wholenum}{project_config.csv_output_sep}" \
                   f"{self.img}{project_config.csv_output_sep}" \
                   f"{self.src}"
        return csv_line
