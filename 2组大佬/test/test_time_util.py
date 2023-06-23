# coding:utf-8
"""
测试time_util.py的内容
"""
import time
from unittest import TestCase
from day02.util import time_util

class TestTimeUtil(TestCase):
    def test_get_time(self):
        dt=time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
        r=time_util.get_time()
        self.assertEqual(dt,r)

    def test_get_today(self):
        dt=time.strftime("%Y-%m-%d",time.localtime())
        r=time_util.get_today()
        self.assertEqual(dt,r)

    def test_second_ts_to_date_str(self):
        r=time_util.second_ts_to_date_str(1688659200)
        self.assertEqual("2023-07-07 00:00:00",r)

        r = time_util.second_ts_to_date_str(1688659200,"%Y_%m_%d-%H-%M-%S")
        self.assertEqual("2023_07_07-00-00-00", r)

    def test_millisecond_ts_to_date_str(self):
        r=time_util.millisecond_ts_to_date_str(1688659200000)
        self.assertEqual("2023-07-07 00:00:00", r)

        r = time_util.millisecond_ts_to_date_str(1688659200000, "%Y_%m_%d-%H-%M-%S")
        self.assertEqual("2023_07_07-00-00-00", r)

        r = time_util.millisecond_ts_to_date_str(1688659200034)
        self.assertEqual("2023-07-07 00:00:00", r)

        r = time_util.millisecond_ts_to_date_str(1688659200034, "%Y_%m_%d-%H-%M-%S")
        self.assertEqual("2023_07_07-00-00-00", r)

    def test_str_to_time(self):
        time_str = "2023-06-23 02:43:47.123456"
        t1 = time_util.str_to_time(time_str)
        self.assertEqual("2023-06-23 02:43:47",t1)