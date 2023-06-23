import logging
import os.path
from unittest import TestCase
from util import logging_util


class Test(TestCase):
    def test_get_logger(self):
        logger = logging_util.get_logger(
            log_path=r"F:\study\PycharmProjects\ETL\day01\logs\unittest.log"
        )
        self.assertIsInstance(logger, logging.Logger)
        handles = logger.handlers
        self.assertGreater(len(handles), 0)

        logger.info("hahaha")
        self.assertEqual(True, os.path.exists("F:\study\PycharmProjects\ETL\day01\logs\\unittest.log"))
