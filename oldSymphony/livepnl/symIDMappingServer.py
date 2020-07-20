import csv
import threading
import socketserver
import json
from datetime import datetime

'''Below order is to generate a mapping of Symbol ids and name for XTS API'''


class CsvToDict:

    optionIDSymname = {}
    reader = csv.reader(open(
        r'C:\Users\Mudraksh_Server1\Desktop\ServerCodes\Symphony Latest API\Symphony Order Server Dealer/OptionIds.txt', 'r'))
    for row in reader:
        v1, k = row
        optionIDSymname[k] = v1

    futIDSymname = {}
    reader = csv.reader(open(
        r'C:\Users\Mudraksh_Server1\Desktop\ServerCodes\Symphony Latest API\Symphony Order Server Dealer/FuturesIds.txt', 'r'))
    for row in reader:
        v1, k = row
        futIDSymname[k] = v1
    commodityIDSymname = {}
    reader = csv.reader(open(
        r'C:\Users\Mudraksh_Server1\Desktop\ServerCodes\Symphony Latest API\Symphony Order Server Dealer/MCXIds.txt', 'r'))
    for row in reader:
        v1, k = row
        commodityIDSymname[k] = v1
    stocksIDSymname = {}
    reader = csv.reader(open(
        r'C:\Users\Mudraksh_Server1\Desktop\ServerCodes\Symphony Latest API\Symphony Order Server Dealer/stocksIds.txt', 'r'))
    for row in reader:
        v1, k = row
        stocksIDSymname[k] = v1


obj = CsvToDict()
stocksMap = obj.stocksIDSymname
# if "FORTIS" in stocksMap:
#        print(stocksMap["FORTIS"])
optionMap = obj.optionIDSymname
futureMap = obj.futIDSymname
commodityMap = obj.commodityIDSymname
