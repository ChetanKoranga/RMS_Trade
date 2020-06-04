from pymongo import MongoClient
import pymongo
import datetime
import time
from demoMongo2 import savedata
import csv

date = datetime.date.today()
netq_collec = f'symphonyorder_netquantity_{date}'
# filtered_collec = f'neworders_{date}'
cumulative_collec = f"cumulative_{date}"

connection = MongoClient('localhost', 27017)

try:
    cumulative_db = connection['Cumulative_symphonyorder']
    # new_db = connection['symphonyorder_filtered']

except Exception:
    print("ERROR: Mongo Connection Error123")

try:
    netq_db = connection['symphonyorder_netquantity']
    netq_db[netq_collec].drop()
    print('Netq Collec Deleted')
except:
    pass


class CsvToDict:
    optionIDSymname = {}
    reader = csv.reader(open(
        r'C:\Users\Mudraksh_Server1\Desktop\ServerCodes\test\Symphony Order Server Dealer\OptionIds.txt', 'r'))
    for row in reader:
        v1, k = row
        optionIDSymname[v1] = k

    futIDSymname = {}
    reader = csv.reader(open(
        r'C:\Users\Mudraksh_Server1\Desktop\ServerCodes\test\Symphony Order Server Dealer\FuturesIds.txt', 'r'))
    for row in reader:
        v1, k = row
        futIDSymname[v1] = k

    commodityIDSymname = {}
    reader = csv.reader(open(
        r'C:\Users\Mudraksh_Server1\Desktop\ServerCodes\test\Symphony Order Server Dealer\MCXIds.txt', 'r'))
    for row in reader:
        v1, k = row
        commodityIDSymname[v1] = k

    stocksIDSymname = {}
    reader = csv.reader(open(
        r'C:\Users\Mudraksh_Server1\Desktop\ServerCodes\test\Symphony Order Server Dealer\stocksIds.txt', 'r'))
    for row in reader:
        v1, k = row
        stocksIDSymname[v1] = k


obj = CsvToDict()
stocksMap = obj.stocksIDSymname
optionMap = obj.optionIDSymname
futureMap = obj.futIDSymname
commodityMap = obj.commodityIDSymname


def check_data():
    id_dict = {}
    count = cumulative_db[cumulative_collec].count()
    print(count)
    # while True:

    neworders = cumulative_db[cumulative_collec].find().sort(
        [('_id', -1)]).limit(count)
    for order in neworders:

        order_id = order['_id']

        clientID = order['clientID']
        quantity = order['quantity']
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

        if order_id not in id_dict.keys():
            id_dict.update({order_id: quantity})
            # print(id_dict)

            # print("Not In list")

            try:
                post = {
                    "clientID": clientID,
                    "symbol": symbol,
                    "quantity": quantity,
                }
                # print(post)
                savedata(post, date)
                # print(post)

            except Exception as e:
                print(e)
                continue

        else:

            if ((quantity != id_dict[order_id])):  # and (quantity !=0)):

                try:
                    # quantity = quantity-id_dict[order_id]
                    # print(quantity)
                    post = {"clientID": clientID,
                            "symbol": symbol,
                            "quantity": quantity - id_dict[order_id],
                            }
                    # print(quantity,'+',id_dict[order_id])
                    savedata(post, date)
                    id_dict.update({order_id: quantity})

                except Exception as e:
                    print(e)
                    continue
            '''

            else:
                if (quantity != id_dict[order_id]):
                    try:
                        post = {"clientID": clientID,
                                "symbol": symbol,
                                "quantity": quantity,
                                }
                        savedata(post, date)
                        print(quantity)
                        id_dict.update({order_id: quantity})                        

                    except Exception as e:
                        print (e)
                        continue
            '''


while True:
    check_data()
    time.sleep(1)
    # netq_db[netq_collec].drop()
