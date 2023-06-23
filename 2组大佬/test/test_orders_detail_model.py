# coding:utf8
"""
测试订单详情模型
"""
import json
from unittest import TestCase
from day02.model import orders_model


class TestOrdersDetailModel(TestCase):
    def test_generate_insert_sql(self):
        data_str = '{"discountRate": 1, "storeShopNo": "None", "dayOrderSeq": 37, "storeDistrict": "芙蓉区", ' \
               '"isSigned": 0, "storeProvince": "湖南省", "origin": 0, "storeGPSLongitude": "undefined", ' \
               '"discount": 0, "storeID": 1766, "productCount": 1, "operatorName": "OperatorName", ' \
               '"operator": "NameStr", "storeStatus": "open", "storeOwnUserTel": 12345678910, ' \
               '"payType": "cash", "discountType": 2, "storeName": "亿户超市郭一一食品店", ' \
               '"storeOwnUserName": "OwnUserNameStr", "dateTS": 1542436490000, "smallChange": 0, ' \
               '"storeGPSName": "None", "erase": 0, "product": ' \
               '[{"count": 1, "name": "南京特醇", "unitID": 8, "barcode": "6901028300056", ' \
               '"pricePer": 12, "retailPrice": 12, "tradePrice": 11, "categoryID": 1}], ' \
               '"storeGPSAddress": "None", "orderID": "154243648991517662217", ' \
               '"moneyBeforeWholeDiscount": 12, "storeCategory": "normal", ' \
               '"receivable": 12, "faceID": "", "storeOwnUserId": 1694, ' \
               '"paymentChannel": 0, "paymentScenarios": "OTHER", "storeAddress": "StoreAddress", ' \
               '"totalNoDiscount": 12, "payedTotal": 12, "storeGPSLatitude": "undefined", ' \
               '"storeCreateDateTS": 1540793134000, "storeCity": "长沙市", "memberID": "0"}'
        orders_models = orders_model.OrdersModel(data_str)
        model = orders_models.orders_detail_list[0]
        r = model.generate_insert_sql()
        excepted = "insert into orders_detail(order_id,barcode,name,count,price_per," \
                  "retail_price,trade_price,category_id,unit_id)values('154243648991517662217','6901028300056'," \
                  "'南京特醇',1,12,12,11,1,8)"
        # print(r)
        self.assertEqual(excepted, r)

    def test_get_csv_header(self):
        data_str = '{"discountRate": 1, "storeShopNo": "None", "dayOrderSeq": 37, "storeDistrict": "芙蓉区", ' \
                   '"isSigned": 0, "storeProvince": "湖南省", "origin": 0, "storeGPSLongitude": "undefined", ' \
                   '"discount": 0, "storeID": 1766, "productCount": 1, "operatorName": "OperatorName", ' \
                   '"operator": "NameStr", "storeStatus": "open", "storeOwnUserTel": 12345678910, ' \
                   '"payType": "cash", "discountType": 2, "storeName": "亿户超市郭一一食品店", ' \
                   '"storeOwnUserName": "OwnUserNameStr", "dateTS": 1542436490000, "smallChange": 0, ' \
                   '"storeGPSName": "None", "erase": 0, "product": ' \
                   '[{"count": 1, "name": "南京特醇", "unitID": 8, "barcode": "6901028300056", ' \
                   '"pricePer": 12, "retailPrice": 12, "tradePrice": 11, "categoryID": 1}], ' \
                   '"storeGPSAddress": "None", "orderID": "154243648991517662217", ' \
                   '"moneyBeforeWholeDiscount": 12, "storeCategory": "normal", ' \
                   '"receivable": 12, "faceID": "", "storeOwnUserId": 1694, ' \
                   '"paymentChannel": 0, "paymentScenarios": "OTHER", "storeAddress": "StoreAddress", ' \
                   '"totalNoDiscount": 12, "payedTotal": 12, "storeGPSLatitude": "undefined", ' \
                   '"storeCreateDateTS": 1540793134000, "storeCity": "长沙市", "memberID": "0"}'
        orders_models = orders_model.OrdersModel(data_str)
        model = orders_models.orders_detail_list[0]
        csv_header = model.get_csv_header()
        excepted = "orderID,barcode,name,count,pricePer,retailPrice,tradePrice,categoryID,unitID"
        # print(csv_header)
        self.assertEqual(excepted, csv_header)

    def test_to_csv(self):
        data_str = '{"discountRate": 1, "storeShopNo": "None", "dayOrderSeq": 37, "storeDistrict": "芙蓉区", ' \
                   '"isSigned": 0, "storeProvince": "湖南省", "origin": 0, "storeGPSLongitude": "undefined", ' \
                   '"discount": 0, "storeID": 1766, "productCount": 1, "operatorName": "OperatorName", ' \
                   '"operator": "NameStr", "storeStatus": "open", "storeOwnUserTel": 12345678910, ' \
                   '"payType": "cash", "discountType": 2, "storeName": "亿户超市郭一一食品店", ' \
                   '"storeOwnUserName": "OwnUserNameStr", "dateTS": 1542436490000, "smallChange": 0, ' \
                   '"storeGPSName": "None", "erase": 0, "product": ' \
                   '[{"count": 1, "name": "南京特醇", "unitID": 8, "barcode": "6901028300056", ' \
                   '"pricePer": 12, "retailPrice": 12, "tradePrice": 11, "categoryID": 1}], ' \
                   '"storeGPSAddress": "None", "orderID": "154243648991517662217", ' \
                   '"moneyBeforeWholeDiscount": 12, "storeCategory": "normal", ' \
                   '"receivable": 12, "faceID": "", "storeOwnUserId": 1694, ' \
                   '"paymentChannel": 0, "paymentScenarios": "OTHER", "storeAddress": "StoreAddress", ' \
                   '"totalNoDiscount": 12, "payedTotal": 12, "storeGPSLatitude": "undefined", ' \
                   '"storeCreateDateTS": 1540793134000, "storeCity": "长沙市", "memberID": "0"}'
        orders_models = orders_model.OrdersModel(data_str)
        model = orders_models.orders_detail_list[0]
        csv_line = model.to_csv()
        # print(csv_line)
        excepted = "154243648991517662217,6901028300056,南京特醇,1,12,12,11,1,8"
        self.assertEqual(excepted,csv_line)