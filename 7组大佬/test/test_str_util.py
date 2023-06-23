from unittest import TestCase

from util import str_util


class Test(TestCase):
    def test_check_null(self):
        result = str_util.check_null("")
        self.assertTrue(result)

        result = str_util.check_null(None)
        self.assertTrue(result)

        result = str_util.check_null('None')
        self.assertTrue(result)

        result = str_util.check_null('null')
        self.assertTrue(result)

        result = str_util.check_null('undefined')
        self.assertTrue(result)

    def test_check_null_and_transform_to_sql_null(self):
        result = str_util.check_null_and_transform_to_sql_null("")
        self.assertEqual("null", result)

        result = str_util.check_null_and_transform_to_sql_null(None)
        self.assertEqual("null", result)

        result = str_util.check_null_and_transform_to_sql_null('None')
        self.assertEqual("null", result)

        result = str_util.check_null_and_transform_to_sql_null("null")
        self.assertEqual("null", result)

        result = str_util.check_null_and_transform_to_sql_null("undefined")
        self.assertEqual("null", result)

        result = str_util.check_null_and_transform_to_sql_null("张三")
        self.assertEqual("'张三'", result)

    def test_unite_path_slash(self):
        files = str_util.unite_path_slash(r'D:\files_name/files_name\\files_name//files_name')
        self.assertEqual(r'D:/files_name/files_name/files_name/files_name', files)

    def test_replace_comma(self):
        result = str_util.replace_comma("哥，保时捷新款SUV要来了解一下不")
        self.assertEqual("哥，保时捷新款SUV要来了解一下不", result)

    def test_remove_fist_last(self):
        result = str_util.remove_fist_last("[info]")
        self.assertEqual("info", result)

    def test_remove_millisecond(self):
        result = str_util.remove_millisecond("2023-06-23 09:40:54.040497")
        self.assertEqual("2023-06-23 09:40:54", result)

    def test_fetch_number(self):
        result = str_util.fetch_number("响应时间:10ms")
        self.assertEqual(10, result)
