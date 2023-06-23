import logging
import os
from unittest import TestCase
from untils import logging_util


class TestLogging(TestCase):
    def test_logging(self):
        logger = logging_util.get_logger(
            log_path=r"..\logs\unittest.log"
        )
        self.assertIsInstance(logger, logging.Logger)

        handles = logger.handlers
        self.assertEqual(len(handles), 1)

        logger.info("hahaha")
        self.assertTrue(True, os.path.exists(r"..\logs\unittest.log"))


if __name__ == '__main__':
    TestLogging().test_logging()
