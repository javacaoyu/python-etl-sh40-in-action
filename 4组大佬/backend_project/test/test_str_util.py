from unittest import TestCase
from util import str_util

class Test(TestCase):

    def test_check_null(self):
        r = str_util.check_null(None)
        self.assertTrue(r)

        r = str_util.check_null('None')
        self.assertTrue(r)

        r = str_util.check_null('undefined')
        self.assertTrue(r)

        r = str_util.check_null('abc')
        self.assertFalse(r)

    def test_check_null_transform_to_str(self):
        r = str_util.check_null_transform_to_str('none')
        self.assertEqual('NULL',r)

        r = str_util.check_null_transform_to_str(None)
        self.assertEqual('NULL', r)

        r = str_util.check_null_transform_to_str('undefined')
        self.assertEqual('NULL', r)

        r = str_util.check_null_transform_to_str('abc')
        self.assertEqual("'abc'", r)

    def test_unite_path_slash(self):
        r = str_util.unite_path_slash(r'E:\\a\\\\b//c/d')
        self.assertEqual("E:/a/b/c/d",r)
