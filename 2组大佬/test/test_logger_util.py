# coding:utf8
"""
测试logger_util.py的方法
"""
import logging
import os.path
from unittest import TestCase
from day02.util import logger_util


class TestLoggerUtil(TestCase):
    def test_get_logger(self):
        logger = logger_util.get_logger(
                log_path=r"D:\ETL2\code\day02\test\logs\unittest.log"
        )
        self.assertIsInstance(logger, logging.Logger)
        handlers = logger.handlers
        print(type(handlers[0]))
        self.assertEqual(len(handlers), 1)

        logger.info("hahaha")
        self.assertTrue(True, os.path.exists(r"D:\ETL2\code\day02\test\logs\unittest.log"))
