# coding:utf8
"""
测试字符串相关工具
"""

from unittest import TestCase
from day02.util import str_util


class TestStrUtil(TestCase):
    def test_check_null(self):
        r = str_util.check_null(None)
        self.assertTrue(r)

        r = str_util.check_null("NoNe")
        self.assertTrue(r)

        r = str_util.check_null("")
        self.assertTrue(r)

        r = str_util.check_null("NuLl")
        self.assertTrue(r)

        r = str_util.check_null("uNdeFined")
        self.assertTrue(r)

        r = str_util.check_null("哈哈哈")
        self.assertFalse(r)

    def test_check_null_and_transform_to_sql_null(self):
        r = str_util.check_null_and_transform_to_sql_null("")
        self.assertEqual("NULL", r.upper())

        r = str_util.check_null_and_transform_to_sql_null("None")
        self.assertEqual("NULL", r.upper())

        r = str_util.check_null_and_transform_to_sql_null("NulL")
        self.assertEqual("NULL", r.upper())

        r = str_util.check_null_and_transform_to_sql_null("UndefIned")
        self.assertEqual("NULL", r.upper())

        r = str_util.check_null_and_transform_to_sql_null(None)
        self.assertEqual("NULL", r.upper())

        r = str_util.check_null_and_transform_to_sql_null("哈哈哈哈")
        self.assertEqual("'哈哈哈哈'", r.upper())

    def test_unite_path_slash(self):
        r = str_util.unite_path_slash(r"e:\\a\\b\\c/d")
        self.assertEqual("e:/a/b/c/d", r)

    def test_clean_str(self):
        s1 = "[warning]"
        s = str_util.clean_str(s1)
        self.assertEqual("warning",s)

    def test_respone(self):
        data = "响应时间:786ms"
        tt = str_util.clean_respone(data)
        self.assertEqual(786,tt)
