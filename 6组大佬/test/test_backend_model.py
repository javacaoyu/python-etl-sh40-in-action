from unittest import TestCase
from model.backend_model import BackendModel
from config import db_config


class TestBackendModel(TestCase):
    def test_generate_insert_sql(self):
        data = "2023-06-23 09:55:16.120033	[INFO]	orders_service.py	响应时间:150ms	天津市	和平区	【骚扰短信】我们是专业保洁公司的，哥，您在下沙滨江的别墅需要打扫卫生吗，价格合适，详情：400-618-9090"
        sql = BackendModel(data).generate_insert_sql()
        excepted = "INSERT IGNORE INTO backend(id,backend_time,backend_status,file_name,response_time,province,city,backend_info) values (NULL,'2023-06-23 09:55:16','INFO','orders_service.py','150ms','天津市','和平区','【骚扰短信】我们是专业保洁公司的，哥，您在下沙滨江的别墅需要打扫卫生吗，价格合适，详情：400-618-9090')"
        self.assertEqual(excepted, sql)

    def test_to_csv(self):
        data = "2023-06-23 09:55:16.120033	[INFO]	orders_service.py	响应时间:150ms	天津市	和平区	【骚扰短信】我们是专业保洁公司的，哥，您在下沙滨江的别墅需要打扫卫生吗，价格合适，详情：400-618-9090"
        csv_line = BackendModel(data).to_csv()
        excepted = "2023-06-23 09:55:16,INFO,orders_service.py,150ms,天津市,和平区,【骚扰短信】我们是专业保洁公司的，哥，您在下沙滨江的别墅需要打扫卫生吗，价格合适，详情：400-618-9090"
        self.assertEqual(excepted, csv_line)

    def test_get_csv_header(self):
        csv_head = BackendModel.get_csv_header()
        excepted = "backend_time,backend_status,file_name,response_time,province,city,backend_info"
        self.assertEqual(excepted, csv_head)

