# coding:utf8
"""
list做差
"""
from unittest import TestCase


class TestListDiff(TestCase):
    def test_list_diff(self):
        l1 = [1, 2, 3, 4, 5]
        l2 = [2, 4, 3, 5, 6, 7, 8]
        l3 = set(l2)-set(l1)
        excepeted = {6, 7, 8}
        self.assertEqual(excepeted, l3)
