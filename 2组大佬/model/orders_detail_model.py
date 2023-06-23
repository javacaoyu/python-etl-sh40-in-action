# coding:utf8
"""
订单详情表模型
"""

from day02.config import db_config, project_config


class OrdersDetailModel:
    def __init__(self, order_id, product: dict):

        self.order_id = order_id
        self.barcode = product['barcode']
        self.name = product['name']
        self.count = product['count']
        self.price_per = product['pricePer']
        self.retail_price = product['retailPrice']
        self.trade_price = product['tradePrice']
        self.category_id = product['categoryID']
        self.unit_id = product['unitID']

    def generate_insert_sql(self, table_name=db_config.target_orders_detail_table_name):
        sql = f"insert into {table_name}(" \
              f"order_id,barcode,name,count,price_per,retail_price,trade_price,category_id,unit_id)" \
              f"values(" \
              f"\'{self.order_id}\'," \
              f"\'{self.barcode}\'," \
              f"\'{self.name}\'," \
              f"{self.count}," \
              f"{self.price_per}," \
              f"{self.retail_price}," \
              f"{self.trade_price}," \
              f"{self.category_id}," \
              f"{self.unit_id})"
        return sql

    def to_csv(self, sep=project_config.csv_output_sep):
        csv_line = f"{self.order_id}{sep}" \
                   f"{self.barcode}{sep}" \
                   f"{self.name}{sep}" \
                   f"{self.count}{sep}" \
                   f"{self.price_per}{sep}" \
                   f"{self.retail_price}{sep}" \
                   f"{self.trade_price}{sep}" \
                   f"{self.category_id}{sep}" \
                   f"{self.unit_id}"
        return csv_line

    @staticmethod
    def get_csv_header():
        order_detail_csv_str = f"orderID{project_config.csv_output_sep}" \
                               f"barcode{project_config.csv_output_sep}" \
                               f"name{project_config.csv_output_sep}" \
                               f"count{project_config.csv_output_sep}" \
                               f"pricePer{project_config.csv_output_sep}" \
                               f"retailPrice{project_config.csv_output_sep}" \
                               f"tradePrice{project_config.csv_output_sep}" \
                               f"categoryID{project_config.csv_output_sep}" \
                               f"unitID"
        return order_detail_csv_str
