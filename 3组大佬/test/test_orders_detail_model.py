import json
from unittest import TestCase
from model import orders_model

class TestOrderDetailModel(TestCase):
    def test_generate_insert_sql_and_to_csv(self):
        data = '{"discountRate": 1, "storeShopNo": "None", "dayOrderSeq": 37, "storeDistrict": "鼎城区",' \
               ' "isSigned": 0, "storeProvince": "湖南省", "origin": 0, "storeGPSLongitude": "111.69035815549377", ' \
               '"discount": 0, "storeID": 2365, "productCount": 1, "operatorName": "OperatorName", ' \
               '"operator": "NameStr", "storeStatus": "open", "storeOwnUserTel": 12345678910, "payType": "cash",' \
               ' "discountType": 2, "storeName": "聚乐购", "storeOwnUserName": "OwnUserNameStr", ' \
               '"dateTS": 1542438424000, "smallChange": 0, "storeGPSName": "None", "erase": 0, ' \
               '"product": [{"count": 2, "name": "百岁山天然矿泉水570ml", "unitID": 0, "barcode": "6922255451427",' \
               ' "pricePer": 3, "retailPrice": 3, "tradePrice": 0, "categoryID": 1}], "storeGPSAddress": "None", ' \
               '"orderID": "154243842352723652622", "moneyBeforeWholeDiscount": 6, "storeCategory": "normal",' \
               ' "receivable": 6, "faceID": "", "storeOwnUserId": 2307, "paymentChannel": 0, ' \
               '"paymentScenarios": "OTHER", "storeAddress": "StoreAddress", "totalNoDiscount": 6, "payedTotal": 6,' \
               ' "storeGPSLatitude": "28.995375630318087", "storeCreateDateTS": 1542268754000, "storeCity": "常德市",' \
               ' "memberID": "0"}'
        data_dict = json.loads(data)
        model = orders_model.OrdersDetailModel(data_dict['orderID'],data_dict['product'][0])
        excepted = "insert into orders_detail values('154243842352723652622' ,'6922255451427' ,'百岁山天然矿泉水570ml' " \
                   ",2 ,3 ,3 ,0 ,1 ,0)"
        self.assertEqual(excepted,model.generate_insert_sql())
        excepted = "154243842352723652622,6922255451427,百岁山天然矿泉水570ml,2,3,3,0,1,0"
        self.assertEqual(excepted,model.to_csv())


