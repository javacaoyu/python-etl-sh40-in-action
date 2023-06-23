from unittest import TestCase
from util import str_util

class Test(TestCase):
    def test_check_null(self):
        r = str_util.check_null("")
        self.assertTrue(r)

        r = str_util.check_null(None)
        self.assertTrue(r)

        r = str_util.check_null("NULL")
        self.assertTrue(r)

        r = str_util.check_null("NoNe")
        self.assertTrue(r)

        r = str_util.check_null("Undefined")
        self.assertTrue(r)

        r = str_util.check_null("abcd")
        self.assertFalse(r)

    def test_check_null_and_transform_to_sql_null(self):
        r = str_util.check_null_and_transform_to_sql_null("")
        self.assertEqual("NULL", r)

        r = str_util.check_null_and_transform_to_sql_null(None)
        self.assertEqual("NULL", r)

        r = str_util.check_null_and_transform_to_sql_null("NULL")
        self.assertEqual("NULL", r)

        r = str_util.check_null_and_transform_to_sql_null("NoNe")
        self.assertEqual("NULL", r)

        r = str_util.check_null_and_transform_to_sql_null("Undefined")
        self.assertEqual("NULL", r)

        r = str_util.check_null_and_transform_to_sql_null("abcd")
        self.assertEqual("'abcd'", r)

    def test_unite_path_slash(self):
        path = r"E://a\b\\c/d"
        r = str_util.unite_path_slash(path)
        self.assertEqual(r"E:/a/b/c/d", r)
        