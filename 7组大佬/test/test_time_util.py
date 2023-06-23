import time
from unittest import TestCase
from util import time_util


class Test(TestCase):
    def test_get_time(self):
        date_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        get_time = time_util.get_time()
        self.assertEqual(date_time, get_time)

    def test_get_today(self):
        date = time.strftime('%Y-%m-%d', time.localtime())
        get_today = time_util.get_today()
        self.assertEqual(date, get_today)

    def test_second_ts_to_date_str(self):
        date_time = time_util.second_ts_to_date_str(1688659200)
        self.assertEqual('2023-07-07 00:00:00', date_time)
        
    def test_millisecond_ts_to_date_str(self):
        date_time = time_util.millisecond_ts_to_date_str(1688659200000)
        self.assertEqual('2023-07-07 00:00:00', date_time)
