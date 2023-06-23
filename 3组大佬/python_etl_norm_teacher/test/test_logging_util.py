import logging
import os.path
from unittest import TestCase
from util import logging_util


class Test(TestCase):

    def test_get_logger(self):
        logger = logging_util.get_logger(
            log_path=r"D:\python-object\python_ETL\python_etl_full_teacher\python_etl_norm_teacher\logs\unittest.log"
        )
        self.assertIsInstance(logger, logging.Logger)
        handles = logger.handlers
        self.assertEqual(len(handles), 1)

        logger.info("hahaha")
        self.assertTrue(True, os.path.exists(r"D:\python-object\python_ETL\python_etl_full_teacher\python_etl_norm_teacher\logs\unittest.log"))