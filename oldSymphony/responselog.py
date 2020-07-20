import json
import ast
import pymongo
from pymongo import MongoClient
import datetime
import time
import csv
from bson import ObjectId

date = datetime.date.today()

# final_responses='final_response_'+str(date)

connection = MongoClient()


class CsvToDict:

    optionIDSymname = {}
    reader = csv.reader(open(
        r'C:\Users\Mudraksh_Server1\Desktop\ServerCodes\Symphony Latest API\Symphony Order Server Dealer\OptionIds.txt', 'r'))
    for row in reader:
        v1, k = row
        optionIDSymname[v1] = k

    futIDSymname = {}
    reader = csv.reader(open(
        r'C:\Users\Mudraksh_Server1\Desktop\ServerCodes\Symphony Latest API\Symphony Order Server Dealer\FuturesIds.txt', 'r'))
    for row in reader:
        v1, k = row
        futIDSymname[v1] = k

    commodityIDSymname = {}
    reader = csv.reader(open(
        r'C:\Users\Mudraksh_Server1\Desktop\ServerCodes\Symphony Latest API\Symphony Order Server Dealer\MCXIds.txt', 'r'))
    for row in reader:
        v1, k = row
        commodityIDSymname[v1] = k

    stocksIDSymname = {}
    reader = csv.reader(open(
        r'C:\Users\Mudraksh_Server1\Desktop\ServerCodes\Symphony Latest API\Symphony Order Server Dealer\stocksIds.txt', 'r'))
    for row in reader:
        v1, k = row
        stocksIDSymname[v1] = k


obj = CsvToDict()
stocksMap = obj.stocksIDSymname
optionMap = obj.optionIDSymname
futureMap = obj.futIDSymname
commodityMap = obj.commodityIDSymname


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)


# raw database of requested orders
raw_db = connection['symphonyorder_raw'][f'orders_{date}']


# database having broker response
responsedb = connection[f'order_log_raw_{date}']['order_log_raw']

# final database for visualization in table
final_response = connection['final_response'][f'final_response_{date}']

start_time = time.time()

half_filled_id = []
completed_orders = []
print("Code running...............")
while True:
    current_time = time.time()
    false_orders = raw_db.find({"responseFlag": False})
    if false_orders:
        for order in false_orders:
            order_id = order['orderUniqueIdentifier']
            ordered_time = order['orderSentTime']
            quantity = order['orderQuantity']
            algoname = order['algoName']
            instrumentID = order['exchangeInstrumentID']
            exchangeInstrumentID = order['exchangeInstrumentID']
            orderside = order['orderSide']

            if current_time - ordered_time > 60:
                print(current_time - ordered_time)
                with open('missed_orders.txt', 'a') as outfile:
                    json.dump(JSONEncoder().encode(order), outfile)
                    raw_db.update({'_id': order['_id']}, {
                                  "$set": {'responseFlag': True}})

            resp_data = responsedb.find({'OrderUniqueIdentifier': order_id})
            for resp_order in resp_data:
                OrderUniqueIdentifier = resp_order['OrderUniqueIdentifier']
                orderstatus = resp_order['OrderStatus']
                responseorderquantity = resp_order['OrderQuantity']
                cancelrejectreason = resp_order['CancelRejectReason']
                # quantitybroker = responseDataValue['OrderQuantity']
                rejectedquantity = resp_order['CumulativeQuantity']
                OrderAverageTradedPrice = resp_order['OrderAverageTradedPrice']
                ClientID = resp_order['ClientID']
                LeavesQuantity = resp_order['LeavesQuantity']
                ExchangeSegment = resp_order['ExchangeSegment']
                ProductType = resp_order['ProductType']

                symbolID = str(instrumentID)
                if symbolID in futureMap.keys():
                    symbol = futureMap[symbolID]

                elif symbolID in optionMap.keys():
                    symbol = optionMap[symbolID]

                elif symbolID in commodityMap.keys():
                    symbol = commodityMap[symbolID]

                elif symbolID in stocksMap.keys():
                    symbol = stocksMap[symbolID]
                else:
                    symbol = symbolID

                if LeavesQuantity == 0 or LeavesQuantity == quantity or LeavesQuantity == responseorderquantity:
                    print("FILLED =====", resp_order)
                    raw_db.update({'_id': order['_id']}, {
                                  "$set": {'responseFlag': True}})
                    # if resp_order['_id'] in half_filled_id:
                    #     list.remove(resp_order['_id'])
                    check = responsedb.find(
                        {'OrderUniqueIdentifier': resp_order['OrderUniqueIdentifier']})
                    for res in check:
                        if res['_id'] in half_filled_id:
                            half_filled_id.remove(resp_order['_id'])
                    final_post = {
                        'quantity': quantity,
                        'algoname': algoname,
                        'symbol': symbol,
                        'exchangeInstrumentID': exchangeInstrumentID,
                        'exchangeSegment': ExchangeSegment,
                        'buy_sell': orderside,
                        'time_stamp': str(datetime.datetime.now().time()),
                        'productType': ProductType,
                        'orderStatus': orderstatus,
                        'cancelrejectreason': cancelrejectreason,
                        # 'rejectedquantity': raw_response_dict[orderid]['rejectedquantity']
                        'OrderAverageTradedPrice': OrderAverageTradedPrice,
                        'clientID': ClientID
                    }
                    final_response.insert(final_post)
                    break

                else:
                    if resp_order['_id'] not in half_filled_id:
                        final_post = {
                            'quantity': quantity,
                            'algoname': algoname,
                            'symbol': symbol,
                            'exchangeInstrumentID': exchangeInstrumentID,
                            'exchangeSegment': ExchangeSegment,
                            'buy_sell': orderside,
                            'time_stamp': str(datetime.datetime.now().time()),
                            'productType': ProductType,
                            'orderStatus': orderstatus,
                            'cancelrejectreason': cancelrejectreason,
                            # 'rejectedquantity': raw_response_dict[orderid]['rejectedquantity']
                            'OrderAverageTradedPrice': OrderAverageTradedPrice,
                            'clientID': ClientID
                        }
                        final_response.insert(final_post)
                        half_filled_id.append(resp_order['_id'])
