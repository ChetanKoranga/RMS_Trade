import json
import ast
import pymongo
from pymongo import MongoClient
import datetime
import time
import csv

date = datetime.date.today()

# final_responses='final_response_'+str(date)

connection = MongoClient()
resp_db = f'order_log_raw_{date}'
# final database for visualization in table
final_response = connection.final_response
raw_db = connection.symphonyorder_raw   		# raw database of requested orders
responsedb = connection[resp_db]		# database having broker response

collec = f'orders_{date}'
responsedb_collec = 'order_log_raw'
final_response_collec = 'final_response_'+str(date)
# final_response.create_collection(final_response_collec)


try:
    final_response.create_collection('final_response_'+str(date))
except Exception as e:
    print(e)
    pass

raw_dict = {}
raw_response_dict = {}
old_value_count = raw_db[collec].count()
oldresponse_count = responsedb[responsedb_collec].count()


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

# list_unique = []

while True:

    orderid_list = []
    time.sleep(1)
    newvalue_count = raw_db[collec].count()
    # print("New val:",newvalue_count)
    if old_value_count < newvalue_count:
        new_data = newvalue_count-old_value_count
        # print('new data',new_data)
        new_data_value = raw_db[collec].find().sort(
            [('_id', -1)]).limit(new_data)
        # print('asdf',new_data_value)
        old_value_count = newvalue_count

        for order in new_data_value:
            print('ORDERS:  ', order)
            # extract algoname  frontend:algoname,symbol,quantity(raw_databae),timestamp,buy_sell,orderstatus,rejected_quantity
            identifier = order['orderUniqueIdentifier']
            quantity = order['orderQuantity']
            algoname = order['algoName']
            instrumentID = order['exchangeInstrumentID']
            exchangeInstrumentID = order['exchangeInstrumentID']
            orderside = order['orderSide']
            post = {
                identifier: {
                    'quantity': quantity,
                    'algoname': algoname,
                    'instrumentID': instrumentID,
                    'orderside': orderside,
                    'exchangeInstrumentID': exchangeInstrumentID
                }
            }
            raw_dict.update(post)
        # print('RAWDICT: ',raw_dict)

        # symbol:mapping exchangeinstumentid socketflask
    if raw_dict:
        newresponse_count = responsedb[responsedb_collec].count()
        print('NEW RESPONSE:  ', newresponse_count)
        if newresponse_count > oldresponse_count:
            new_responsedata = newresponse_count-oldresponse_count
            oldresponse_count = newresponse_count
            responseDataValue = responsedb[responsedb_collec].find().sort(
                [('_id', -1)]).limit(new_responsedata)
            for response in responseDataValue:
                timestamp = datetime.datetime.now().time()
                orderuniqueidentifier = response['OrderUniqueIdentifier']
                orderstatus = response['OrderStatus']
                responseorderquantity = response['OrderQuantity']
                cancelrejectreason = response['CancelRejectReason']
                # quantitybroker = responseDataValue['OrderQuantity']
                rejectedquantity = response['CumulativeQuantity']
                OrderAverageTradedPrice = response['OrderAverageTradedPrice']
                ClientID = response['ClientID']
                LeavesQuantity = response['LeavesQuantity']
                ExchangeSegment = response['ExchangeSegment']
                ProductType = response['ProductType']

                response_post = {
                    orderuniqueidentifier: {
                        'timestamp': str(timestamp),
                        'orderstatus': orderstatus,
                        'ProductType': ProductType,
                        'cancelrejectreason': cancelrejectreason,
                        'OrderQuantity': responseorderquantity-LeavesQuantity,
                        # 'rejectedquantity': rejectedquantity,
                        'OrderAverageTradedPrice': OrderAverageTradedPrice,
                        'ClientID': ClientID,
                        'LeavesQuantity': LeavesQuantity,
                        'ExchangeSegment': ExchangeSegment,
                        'OrderStatus': orderstatus
                    }
                }
                # print('RESPOST: ',response_post)
                raw_response_dict.update(response_post)

                for orderid in raw_dict.keys():
                    # print('OrderID:', orderid)
                    # print('Response Dict:', raw_response_dict)
                    foundFlag = False
                    if str(orderid) in raw_response_dict.keys():
                        # print('ID found')
                        # print('OrderStatus:', raw_response_dict[orderid])
                        if raw_response_dict[orderid]['orderstatus'] == "Filled" or raw_response_dict[orderid]['orderstatus'] == "Rejected" or raw_response_dict[orderid]['orderstatus'] == "Cancelled":
                            print('checked status')

                            symbolID = str(raw_dict[orderid]['instrumentID'])
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
                            quantity = raw_response_dict[orderid]['OrderQuantity']
                            if raw_response_dict[orderid]['orderstatus'] == "Rejected" or raw_response_dict[orderid]['orderstatus'] == "Cancelled":
                                quantity = raw_response_dict[orderid]['LeavesQuantity']
                                tempID = orderid
                                orderid_list.append(orderid)
                                foundFlag = True
                            elif raw_response_dict[orderid]['LeavesQuantity'] == 0:
                                orderid_list.append(orderid)
                                tempID = orderid
                                foundFlag = True
                            elif raw_response_dict[orderid]['LeavesQuantity'] != 0:
                                tempID = orderid
                            # else:
                            # 	list_unique.append(orderid)

                            final_post = {
                                'quantity': quantity,
                                'algoname': raw_dict[tempID]['algoname'],
                                'symbol': symbol,
                                'exchangeInstrumentID': raw_dict[tempID]['exchangeInstrumentID'],
                                'exchangeSegment': raw_response_dict[tempID]['ExchangeSegment'],
                                'buy_sell': raw_dict[tempID]['orderside'],
                                'time_stamp': raw_response_dict[tempID]['timestamp'],
                                'productType': raw_response_dict[tempID]['ProductType'],
                                'orderStatus': raw_response_dict[tempID]['OrderStatus'],
                                'cancelrejectreason': raw_response_dict[tempID]['cancelrejectreason'],
                                # 'rejectedquantity': raw_response_dict[orderid]['rejectedquantity']
                                'OrderAverageTradedPrice': raw_response_dict[tempID]['OrderAverageTradedPrice'],
                                'clientID': raw_response_dict[tempID]['ClientID']
                            }
                            print(final_post)
                            final_response[final_response_collec].insert_one(
                                final_post)
                            # final_response.'final_response_'+str(date).insert_one(final_post)
                            if foundFlag:
                                del raw_response_dict[orderid]
                                foundFlag = False
                    # elif raw_response_dict[orderid]['orderstatus'] == "Rejected":

            if orderid_list:
                for ord in orderid_list:
                    del raw_dict[ord]
