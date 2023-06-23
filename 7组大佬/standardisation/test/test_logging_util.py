import logging
import os.path
from unittest import TestCase
from util import logging_util


class Test(TestCase):
    def test_get_logger(self):
        logger = logging_util.get_logger(
            log_path=r'D:\PycharmProjects\log\log_test.log'
        )
        self.assertIsInstance(logger, logging.Logger)

        handles = logger.handlers
        self.assertEqual(len(handles), 1)

        logger.info("测试程序")
        self.assertEqual(True, os.path.exists(r'D:\PycharmProjects\log\log_test.log'))
