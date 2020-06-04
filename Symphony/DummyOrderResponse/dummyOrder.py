from pymongo import MongoClient
import pymongo
import datetime
# from demoMongo import savedata
import csv
import time
from uniqueIdentifier import UniqueIdentifier
from random import randint

time_stamp = str(datetime.datetime.now().time())
date = datetime.date.today()

raw_collec = f'orders_{date}'
resp_db = f'order_log_raw_{date}'
responsedb_collec = 'order_log_raw'

connection = MongoClient('localhost', 27017)

try:
    raw_db = connection['symphonyorder_raw']
    raw_db.create_collection(raw_collec)
   
except Exception as e:
    print(e)
    pass


try:
    # print("hhhahahah")
    responsedb = connection[resp_db]
    responsedb.create_collection(responsedb_collec)
except Exception as e:
	# print(e)
	pass

orderstatus = ["Cancelled"]
OrderUniqueIdentifier = str(UniqueIdentifier())
print(OrderUniqueIdentifier)
orderquantity = 200
leavesQuantity = 0





dummy_orderpost = {
    "exchangeSegment":"NSEFO",
    "exchangeInstrumentID":"47564",
    "productType":"MIS",
    "orderType":"MARKET",
    "orderSide":"BUY",
    "timeInForce":"DAY",
    "disclosedQuantity":0,
    "orderQuantity":orderquantity,
    "limitPrice":0,
    "stopPrice":0,
    "clientID":"D7730002",
    "orderUniqueIdentifier":OrderUniqueIdentifier,
    "algoName":"Straddle Write 4x"
}

raw_db[raw_collec].insert_one(dummy_orderpost)


dummy_responsepost = {
    "LoginID":"D7730001",
    "ClientID":"D7730002",
    "AppOrderID":901464450,
    "OrderReferenceID":"",
    "GeneratedBy":"TWSAPI",
    "ExchangeOrderID":"",
    "OrderCategoryType":"NORMAL",
    "ExchangeSegment":"NSEFO",
    "ExchangeInstrumentID":48186,
    "OrderSide":"Sell",
    "OrderType":"Market",
    "ProductType":"MIS",
    "TimeInForce":"DAY",
    "OrderPrice":0,
    "OrderQuantity":orderquantity,
    "OrderStopPrice":0,
    "OrderStatus":"Filled",
    "OrderAverageTradedPrice":"",
    "LeavesQuantity":leavesQuantity,
    "CumulativeQuantity":0,
    "OrderDisclosedQuantity":0,
    "OrderGeneratedDateTime":f"{date}T{time}",
    "ExchangeTransactTime":f"{date}T{time}+05:30",
    "LastUpdateDateTime":f"{date}T{time}",
    "OrderExpiryDate":"0001-01-01T00:00:00",
    "CancelRejectReason":"",
    "OrderUniqueIdentifier":OrderUniqueIdentifier,
    "OrderLegStatus":"SingleOrderLeg",
    "MessageCode":9004,
    "MessageVersion":4,
    "TokenID":0,
    "ApplicationType":146,
    "SequenceNumber":-1
}
responsedb[responsedb_collec].insert_one(dummy_responsepost)

if leavesQuantity > 0:
    orderstatus = orderstatus[0]
    CancelRejectReason = "Out of Range"
    # if orderstatus == "Rejected":
    #     CancelRejectReason = "Reject ho gya"
    dummy_responsepost = {
    "LoginID":"D7730001",
    "ClientID":"D7730002",
    "AppOrderID":901464450,
    "OrderReferenceID":"",
    "GeneratedBy":"TWSAPI",
    "ExchangeOrderID":"",
    "OrderCategoryType":"NORMAL",
    "ExchangeSegment":"NSEFO",
    "ExchangeInstrumentID":48186,
    "OrderSide":"Sell",
    "OrderType":"Market",
    "ProductType":"MIS",
    "TimeInForce":"DAY",
    "OrderPrice":0,
    "OrderQuantity":orderquantity,
    "OrderStopPrice":0,
    "OrderStatus":orderstatus,
    "OrderAverageTradedPrice":"",
    "LeavesQuantity":leavesQuantity,
    "CumulativeQuantity":0,
    "OrderDisclosedQuantity":0,
    "OrderGeneratedDateTime":f"{date}T{time}",
    "ExchangeTransactTime":f"{date}T{time}+05:30",
    "LastUpdateDateTime":f"{date}T{time}",
    "OrderExpiryDate":"0001-01-01T00:00:00",
    "CancelRejectReason":CancelRejectReason,
    "OrderUniqueIdentifier":OrderUniqueIdentifier,
    "OrderLegStatus":"SingleOrderLeg",
    "MessageCode":9004,
    "MessageVersion":4,
    "TokenID":0,
    "ApplicationType":146,
    "SequenceNumber":-1
    }
    responsedb[responsedb_collec].insert_one(dummy_responsepost)