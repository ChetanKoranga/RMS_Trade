import json
import ast
import pymongo
from pymongo import MongoClient
import datetime
import time
import csv
import winsound
import playsound
from check_alarm import alarm_reason

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


date = datetime.date.today()

connection = MongoClient()

raw_db = connection.symphonyorder_raw   		# raw database of requested orders

raw_collec = f'orders_{date}'

clientOrder_collec = f"client_orders_{date}"
clientOrder_db = connection.client_order_log[clientOrder_collec]


id_list = []


def initialStartup():
    try:
        clientOrder_db.drop()
        print('client_order_log collec Deleted')
    except:
        pass

    count = clientOrder_db.count()

    neworders = raw_db[raw_collec].find().sort([('_id', -1)]).limit(count)
    # print(neworders)
    # data.append(neworders)
    # old_count = new_count

    for order in neworders:
        # print("Orders : ",order)
        order_id = order['_id']

        if order_id not in id_list:
            id_list.append(order_id)

            print('ORDERS:  ', order)
            # extract algoname  frontend:algoname,symbol,quantity(raw_databae),timestamp,buy_sell,orderstatus,rejected_quantity
            identifier = order['orderUniqueIdentifier']
            quantity = order['orderQuantity']
            algoname = order['algoName']
            productType = order['productType']
            instrumentID = order['exchangeInstrumentID']
            exchangeInstrumentID = order['exchangeInstrumentID']
            orderside = order['orderSide']
            clientID = order['clientID']
            epoch = order['orderSentTime']
            timestamp = time.strftime('%H:%M:%S', time.localtime(epoch))
            symbolID = str(exchangeInstrumentID)
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

            post = {
                'quantity': quantity,
                'algoname': algoname,
                'instrumentID': instrumentID,
                'orderside': orderside,
                'exchangeInstrumentID': exchangeInstrumentID,
                'productType': productType,
                'clientID': clientID,
                'symbol': symbol,
                'orderstatus': "Order Sent",
                'timestamp': timestamp,
                'identifier': identifier
            }

            # raw_dict.update(post)
            clientOrder_db.insert_one(post)
    print('Initial==========')


initialStartup()

count = 200

while True:
    neworders = raw_db[raw_collec].find().sort([('_id', -1)]).limit(count)
    # print(neworders)
    # data.append(neworders)
    # old_count = new_count
    id_list_length = len(id_list)
    for order in neworders:
        # print("Orders : ",order)
        order_id = order['_id']

        if order_id not in id_list:
            id_list.append(order_id)
            # playsound.playsound("beep.mp3")
            # playsound.playsound("beep.mp3")

            print('ORDERS:  ', order)
            # extract algoname  frontend:algoname,symbol,quantity(raw_databae),timestamp,buy_sell,orderstatus,rejected_quantity
            identifier = order['orderUniqueIdentifier']
            quantity = order['orderQuantity']
            algoname = order['algoName']
            productType = order['productType']
            instrumentID = order['exchangeInstrumentID']
            exchangeInstrumentID = order['exchangeInstrumentID']
            orderside = order['orderSide']
            clientID = order['clientID']
            epoch = order['orderSentTime']
            timestamp = time.strftime('%H:%M:%S', time.localtime(epoch))
            symbolID = str(exchangeInstrumentID)
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

            post = {
                'quantity': quantity,
                'algoname': algoname,
                'instrumentID': instrumentID,
                'orderside': orderside,
                'exchangeInstrumentID': exchangeInstrumentID,
                'productType': productType,
                'clientID': clientID,
                'symbol': symbol,
                'orderstatus': "Order Sent",
                'timestamp': timestamp,
                'identifier': identifier
            }

            # raw_dict.update(post)
            clientOrder_db.insert_one(post)
    if len(id_list) > id_list_length:
        
        alarm_reason("8","notification","clientOrdersFeed","server system","new order in algo signal feed")
        playsound.playsound("beep.mp3")
        playsound.playsound("beep.mp3")
