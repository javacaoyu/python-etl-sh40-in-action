import os
from unittest import TestCase
from util import file_unit


class Test(TestCase):
    def setUp(self) -> None:
        # 确认单元测试的文件夹是否存在，不存在，创建
        self.unittest_root_path = f"{os.path.dirname(os.getcwd())}/test/unittest"
        if not os.path.exists(self.unittest_root_path):
            os.mkdir(self.unittest_root_path)

    def test_change_file_suffix(self):
        # 创建测试文件
        test_file_path = self.unittest_root_path + "/" + "test.csv.tmp"
        if not os.path.exists(test_file_path):
            open(test_file_path, 'w', encoding='utf8').close()
        # 确认目标文件不存在，如果存在，删除
        target_file_path = self.unittest_root_path + "/" + "test.csv"
        if os.path.exists(target_file_path):
            os.remove(target_file_path)

        file_unit.change_file_suffix(test_file_path, "", ".tmp")
        self.assertTrue(os.path.exists(self.unittest_root_path + "/" + "test.csv"))

        os.remove(target_file_path)

