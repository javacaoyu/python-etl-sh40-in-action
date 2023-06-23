"""
测试time_unit.py的内容
"""
from unittest import TestCase
from util import time_util
import time


class Test(TestCase):

    def test_get_time(self):
        dt = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        r = time_util.get_time()
        self.assertEqual(dt, r)

    def test_get_today(self):
        dt = time.strftime("%Y-%m-%d", time.localtime())
        r = time_util.get_today()
        self.assertEqual(dt, r)

    def test_millisecond_ts_to_date_str(self):
        dt = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(1687222249))
        r = time_util.millisecond_ts_to_date_str(1687222249000)
        self.assertEqual(dt, r)

        dt = time.strftime("%Y-%m-%d", time.localtime(1687222249000 / 1000))
        r = time_util.millisecond_ts_to_date_str(1687222249000, "%Y-%m-%d")
        self.assertEqual(dt, r)

    def test_second_ts_to_date_str(self):
        dt = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(1687222249))
        r = time_util.second_ts_to_date_str(1687222249)
        self.assertEqual(dt, r)

        dt = time.strftime("%Y-%m-%d", time.localtime(1687222249))
        r = time_util.second_ts_to_date_str(1687222249, "%Y-%m-%d")
        self.assertEqual(dt, r)

