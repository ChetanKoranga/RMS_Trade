from pymongo import MongoClient
import pymongo
import datetime
from demoMongo import savedata
import csv
import time

# from queue import Queue

# old_count = 0
date = datetime.date.today()
raw_collec = f'final_response_{date}'
filtered_collec = f'neworders_{date}'
cumulative_collec = f"cumulative_{date}"

connection = MongoClient('localhost', 27017)

try:
    db = connection['final_response']
    # print(db[raw_collec].find())
    new_db = connection['symphonyorder_filtered']
    # old_count = db['orders_2019-10-15'].count()
except Exception:
    print("ERROR: Mongo Connection Error123")

try:
    cumulative_db = connection['Cumulative_symphonyorder']
    cumulative_db[cumulative_collec].drop()
    print('Cumulative Collec Deleted')
except:
    pass


class CsvToDict:
    optionIDSymname = {}
    reader = csv.reader(open(r'C:\Users\Mudraksh_Server1\Desktop\ServerCodes\test\Symphony Order Server Dealer\OptionIds.txt', 'r'))
    for row in reader:
        v1, k = row
        optionIDSymname[v1] = k

    futIDSymname = {}
    reader = csv.reader(open(r'C:\Users\Mudraksh_Server1\Desktop\ServerCodes\test\Symphony Order Server Dealer\FuturesIds.txt', 'r'))
    for row in reader:
        v1, k = row
        futIDSymname[v1] = k

    commodityIDSymname = {}
    reader = csv.reader(open(r'C:\Users\Mudraksh_Server1\Desktop\ServerCodes\test\Symphony Order Server Dealer\MCXIds.txt', 'r'))
    for row in reader:
        v1, k = row
        commodityIDSymname[v1] = k

    stocksIDSymname = {}
    reader = csv.reader(open(r'C:\Users\Mudraksh_Server1\Desktop\ServerCodes\test\Symphony Order Server Dealer\stocksIds.txt', 'r'))
    for row in reader:
        v1, k = row
        stocksIDSymname[v1] = k


obj = CsvToDict()
stocksMap = obj.stocksIDSymname
optionMap = obj.optionIDSymname
futureMap = obj.futIDSymname
commodityMap = obj.commodityIDSymname


# print(futureMap'')
def check_data():
    # old_count = db[raw_collec].count()
    # data = []
    # que = Queue()
    id_list = []
    count = 100
    print("Engine is running......")
    while True:

        neworders = db[raw_collec].find().sort([('_id', -1)]).limit(count)
        # print(neworders)
        # data.append(neworders)
        # old_count = new_count

        for order in neworders:
            # print("Orders : ",order)
            order_id = order['_id']

            if order_id not in id_list:
                id_list.append(order_id)
                # print("Queue DATA ====== ",a)
                try:
                    exchangeSegment = order['exchangeSegment']
                    clientID = order['clientID']
                    algoname = order['algoname']
                    exchangeInstrumentID = order['exchangeInstrumentID']
                    productType = order['productType']
                    symbolID = str(order['exchangeInstrumentID'])
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

                    quantity = order['quantity']
                    buy_sell = order['buy_sell']
                    orderStatus = order['orderStatus']
                    time_stamp = str(datetime.datetime.now().time())
                    post = {
                        "algoName": algoname,
                        "symbol": symbol,
                        "quantity": quantity,
                        "buy_sell": buy_sell,
                        "time_stamp": time_stamp,
                        "clientID": clientID,
                        "exchangeSegment": exchangeSegment,
                        "exchangeInstrumentID":exchangeInstrumentID,
                        "productType" : productType,
                        "orderStatus" : orderStatus
                    }
                    print(post)
                    savedata(post, date)
                    new_db[filtered_collec].insert(post)
                except Exception as e:
                    print (e)
                    continue
        # print('\n')
        # time.sleep(1)


check_data()