# coding = UTF-8
from config import project_config


class BarcodeModel:
    def __init__(self, data_tuple):
        """
        传入一个tuple，按照以下顺序
        -- code
        -- name
        -- spec
        -- trademark
        -- addr
        -- units
        -- factory_name
        -- trade_price
        -- retail_price
        -- updateAt
        -- wholeunit
        -- wholenum
        -- img
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

    def generate_insert_sql(self, table_name):
        sql = f"insert into {table_name} values (" \
              f"{self.code}," \
              f"{self.name}," \
              f"{self.spec}," \
              f"{self.trademark}," \
              f"{self.addr}," \
              f"{self.units}," \
              f"{self.factory_name}," \
              f"{self.trade_price}," \
              f"{self.retail_price}," \
              f"{self.updateAt}," \
              f"{self.wholeunit}," \
              f"{self.wholenum}," \
              f"{self.img}," \
              f"{self.src}" \
              f")"
        return sql

    def to_csv(self, sep=project_config.csv_output_sep):
        line = f"" \
               f"{self.code}{sep}" \
               f"{self.name}{sep}" \
               f"{self.spec}{sep}" \
               f"{self.trademark}{sep}" \
               f"{self.addr}{sep}" \
               f"{self.units}{sep}" \
               f"{self.factory_name}{sep}" \
               f"{self.trade_price}{sep}" \
               f"{self.retail_price}{sep}" \
               f"{self.updateAt}{sep}" \
               f"{self.wholeunit}{sep}" \
               f"{self.wholenum}{sep}" \
               f"{self.img}{sep}" \
               f"{self.src}{sep}" \
               f""
        return line

    @staticmethod
    def get_csv_header():
        line_header = f"code{project_config.csv_output_sep}" \
                      f"name{project_config.csv_output_sep}" \
                      f"spec{project_config.csv_output_sep}" \
                      f"trademark{project_config.csv_output_sep}" \
                      f"addr{project_config.csv_output_sep}" \
                      f"units{project_config.csv_output_sep}" \
                      f"factory_name{project_config.csv_output_sep}" \
                      f"trade_price{project_config.csv_output_sep}" \
                      f"retail_price{project_config.csv_output_sep}" \
                      f"updateAt{project_config.csv_output_sep}" \
                      f"wholeunit{project_config.csv_output_sep}" \
                      f"wholenum{project_config.csv_output_sep}" \
                      f"img{project_config.csv_output_sep}" \
                      f"src{project_config.csv_output_sep}"
        return line_header

