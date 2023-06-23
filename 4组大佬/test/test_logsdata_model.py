from unittest import TestCase
from model.logs_data_model import LogsDataModel

class TestOrdersModel(TestCase):

    def test_get_sql(self):
        data = f'2023-06-23 09:59:07.893293\t[ERROR]\tbarcode_service.py\t响应时间:485ms\t湖北省\t荆州市\t看啥呢，别看日志了，快写代码，说的就是你。'
        model = LogsDataModel(data)
        r = model.get_insert_sql()
        excepted = "insert ignore into logs_data(" \
                   "data_ts,log_level,log_module,response_time,province,city,log_msg) " \
                   "values('2023-06-23 09:59:07','ERROR','barcode_service.py','485ms'," \
                   "'湖北省','荆州市','看啥呢，别看日志了，快写代码，说的就是你。')"

        self.assertEqual(excepted, r)

    def test_to_csv(self):
        data = f'2023-06-23 09:59:07.893293\t[INFO]\torders_service.py\t响应时间:860ms\t广东省\t深圳市\t明天就发工资了，今天大家好好卷。'
        model = LogsDataModel(data)
        r = model.to_csv()
        excepted = "2023-06-23 09:59:07,INFO,orders_service.py,860ms,广东省,深圳市,明天就发工资了，今天大家好好卷。,"

        self.assertEqual(excepted, r)