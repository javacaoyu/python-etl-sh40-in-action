from config import db_config, project_config


class OrdersDetailModel:
    def __init__(self, order_id, product_dict):
        self.order_id = order_id
        self.count = product_dict['count']
        self.name = product_dict['name']
        self.unit_id = product_dict['unitID']
        self.barcode = product_dict['barcode']
        self.price_per = product_dict['pricePer']
        self.retail_price = product_dict['retailPrice']
        self.trade_price = product_dict['tradePrice']
        self.category_id = product_dict['categoryID']

    def generate_insert_sql(self, table_name=db_config.target_orders_detail_table_name):
        sql = f"INSERT INTO {table_name}(" \
              f"order_id, barcode, name, count, price_per, retail_price, " \
              f"trade_price, category_id, unit_id) VALUES(" \
              f"\'{self.order_id}\', " \
              f"\'{self.barcode}\', " \
              f"\'{self.name}\', " \
              f"{self.count}, " \
              f"{self.price_per}, " \
              f"{self.retail_price}, " \
              f"{self.trade_price}, " \
              f"{self.category_id}, " \
              f"{self.unit_id}" \
              f")"
        return sql

    def to_csv(self):
        csv_line = \
            f"{self.order_id}{project_config.csv_output_sep}" \
            f"{self.barcode}{project_config.csv_output_sep}" \
            f"{self.count}{project_config.csv_output_sep}" \
            f"{self.name}{project_config.csv_output_sep}" \
            f"{self.unit_id}{project_config.csv_output_sep}" \
            f"{self.price_per}{project_config.csv_output_sep}" \
            f"{self.retail_price}{project_config.csv_output_sep}" \
            f"{self.trade_price}{project_config.csv_output_sep}" \
            f"{self.category_id}"
        return csv_line

    @staticmethod
    def get_csv_header():
        orders_detail_header_str = \
            f"orderID{project_config.csv_output_sep}" \
            f"barcode{project_config.csv_output_sep}" \
            f"count{project_config.csv_output_sep}" \
            f"name{project_config.csv_output_sep}" \
            f"unitID{project_config.csv_output_sep}" \
            f"pricePer{project_config.csv_output_sep}" \
            f"retailPrice{project_config.csv_output_sep}" \
            f"tradePrice{project_config.csv_output_sep}" \
            f"categoryID"
        return orders_detail_header_str
