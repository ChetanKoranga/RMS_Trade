import pymongo
import datetime
import random
import time

conn = pymongo.MongoClient()

date = datetime.datetime.today().date()
# print(date)
algosignal_db = conn['symphonyorder_raw'][f'orders_{date}']

response_db = conn[f'order_log_raw_{date}']['order_log_raw']

orderstatus = "Rejected"
orderstatus2 = "Cancelled"


orderside = "BUY"
response_orderside = "BUY"
quantity = 150
response_quantity = 150
instrumentID = 42236
response_instrumentID = 42236
clientID = "D7730001"
response_clientID = "D7730001"
OrderUniqueIdentifier = random.randint(1111111111, 9999999999)
print(OrderUniqueIdentifier)
algosignal_post = {
    "exchangeSegment": "NSEFO",
    "exchangeInstrumentID": instrumentID,
    "productType": "MIS",
    "orderType": "MARKET",
    "orderSide": orderside,
    "timeInForce": "DAY",
    "disclosedQuantity": 0,
    "orderQuantity": quantity,
    "limitPrice": 0,
    "stopPrice": 0,
    "clientID": clientID,
    "orderUniqueIdentifier": OrderUniqueIdentifier,
    "algoName": "firstHourReferenceBankNifty",
    "orderSentTime": time.time(),
    "responseFlag": False
}

algosignal_db.insert_one(algosignal_post)


response_post1 = {
    "LoginID": "D77311",
    "ClientID": response_clientID,
    "AppOrderID": 909949337,
    "OrderReferenceID": "",
    "GeneratedBy": "TWSAPI",
    "ExchangeOrderID": "1400000004942984",
    "OrderCategoryType": "NORMAL",
    "ExchangeSegment": "NSEFO",
    "ExchangeInstrumentID": response_instrumentID,
    "OrderSide": response_orderside,
    "OrderType": "Market",
    "ProductType": "MIS",
    "TimeInForce": "DAY",
    "OrderPrice": 0,
    "OrderQuantity": response_quantity,
    "OrderStopPrice": 0,
    "OrderStatus": orderstatus,
    "OrderAverageTradedPrice": "97.95",
    "LeavesQuantity": 0,
    "CumulativeQuantity": 20,
    "OrderDisclosedQuantity": 0,
    "OrderGeneratedDateTime": "2020-06-18T09:22:04.8359074",
    "ExchangeTransactTime": "2020-06-18T09:22:06+05:30",
    "LastUpdateDateTime": "2020-06-18T09:22:04.8559076",
    "OrderExpiryDate": "1980-01-01T00:00:00",
    "CancelRejectReason": "",
    "OrderUniqueIdentifier": OrderUniqueIdentifier,
    "OrderLegStatus": "SingleOrderLeg",
    "IsSpread": False,
    "MessageCode": 9004,
    "MessageVersion": 4,
    "TokenID": 0,
    "ApplicationType": 146,
    "SequenceNumber": -2147466468
}

response_post2 = {
    "LoginID": "D77311",
    "ClientID": response_clientID,
    "AppOrderID": 909949337,
    "OrderReferenceID": "",
    "GeneratedBy": "TWSAPI",
    "ExchangeOrderID": "1400000004942984",
    "OrderCategoryType": "NORMAL",
    "ExchangeSegment": "NSEFO",
    "ExchangeInstrumentID": response_instrumentID,
    "OrderSide": response_orderside,
    "OrderType": "Market",
    "ProductType": "MIS",
    "TimeInForce": "DAY",
    "OrderPrice": 0,
    "OrderQuantity": response_quantity,
    "OrderStopPrice": 0,
    "OrderStatus": orderstatus2,
    "OrderAverageTradedPrice": "97.95",
    "LeavesQuantity": 0,
    "CumulativeQuantity": 20,
    "OrderDisclosedQuantity": 0,
    "OrderGeneratedDateTime": "2020-06-18T09:22:04.8359074",
    "ExchangeTransactTime": "2020-06-18T09:22:06+05:30",
    "LastUpdateDateTime": "2020-06-18T09:22:04.8559076",
    "OrderExpiryDate": "1980-01-01T00:00:00",
    "CancelRejectReason": "",
    "OrderUniqueIdentifier": OrderUniqueIdentifier,
    "OrderLegStatus": "SingleOrderLeg",
    "IsSpread": False,
    "MessageCode": 9004,
    "MessageVersion": 4,
    "TokenID": 0,
    "ApplicationType": 146,
    "SequenceNumber": -2147466468
}

# response_db.insert_one(response_post1)
# response_db.insert_one(response_post2)
