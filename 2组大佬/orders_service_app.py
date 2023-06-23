# coding:utf8
"""
订单数据采集,启动逻辑
"""

from day02.service.orders_service import *

if __name__ == '__main__':
    OrdersService().start()