# coding:utf8
"""
商品（条码库）信息模型
"""

from day02.config.db_config import *
from day02.config.project_config import *
from day02.util.str_util import *

class BarcodeModel:
    def __init__(self, data_tuple=None):
        """
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
        self.update_at = data_tuple[9]
        self.wholeunit = data_tuple[10]
        self.wholenum = data_tuple[11]
        self.img = data_tuple[12]
        self.src = data_tuple[13]


    def generate_insert_sql(self, table_name=source_barcode_table_name):
        sql = f"insert into {table_name}(" \
              f"code,name,spec,trademark,addr,units," \
              f"factory_name,trade_price,retail_price," \
              f"update_at,wholeunit,wholenum,img,src)values(" \
              f"'{self.code}'," \
              f"'{clean_str(self.name)}'," \
              f"'{clean_str(self.spec)}'," \
              f"'{clean_str(self.trademark)}'," \
              f"'{clean_str(self.addr)}'," \
              f"'{clean_str(self.units)}'," \
              f"'{clean_str(self.factory_name)}'," \
              f"'{clean_str(self.trade_price)}'," \
              f"'{clean_str(self.retail_price)}'," \
              f"'{clean_str(self.update_at)}'," \
              f"'{clean_str(self.wholeunit)}'," \
              f"{check_null_and_transform_to_sql_null(self.wholenum)}," \
              f"'{clean_str(self.img)}'," \
              f"'{clean_str(self.src)}'" \
              f")"
        return sql

    @staticmethod
    def get_csv_header(sep=csv_output_sep):
        header = f"code{sep}" \
                 f"name{sep}" \
                 f"spec{sep}" \
                 f"trademark{sep}" \
                 f"addr{sep}" \
                 f"units{sep}" \
                 f"factory_name{sep}" \
                 f"trade_price{sep}" \
                 f"retail_price{sep}" \
                 f"update_at{sep}" \
                 f"wholeunit{sep}" \
                 f"wholenum{sep}" \
                 f"img{sep}" \
                 f"src"
        return header

    def to_csv(self,sep=csv_output_sep):
        csv_line = f"{self.code}{sep}" \
                   f"{self.name}{sep}" \
                   f"{self.spec}{sep}" \
                   f"{self.trademark}{sep}" \
                   f"{self.addr}{sep}" \
                   f"{self.units}{sep}" \
                   f"{self.factory_name}{sep}" \
                   f"{self.trade_price}{sep}" \
                   f"{self.retail_price}{sep}" \
                   f"{self.update_at}{sep}" \
                   f"{self.wholeunit}{sep}" \
                   f"{self.wholenum}{sep}" \
                   f"{self.img}{sep}" \
                   f"{self.src}"



