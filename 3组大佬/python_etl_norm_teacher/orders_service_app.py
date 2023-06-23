# coding:utf8
"""
订单（Json文件）数据采集，启动逻辑
"""
from service.orders_sevice import OrdersService
from service.barcode_server import BarcodeService

if __name__ == '__main__':
    OrdersService().start()
    BarcodeService().start()