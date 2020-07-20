import json, socket, time
import datetime
import pymongo
from pymongo import MongoClient
from symIDMappingServer import commodityMap
from symIDMappingServer import stocksMap
from symIDMappingServer import optionMap
from symIDMappingServer import futureMap
# import symphonyIdFetcher as sif

# print(commodityMap)

idMap = {}
symList = []


date = datetime.date.today()
client = MongoClient()
try:
    db = client["Cumulative_symphonyorder"]
    collec = f"cumulative_{date}"
    db.create_collection(collec)
    print("Database is created")

except Exception as e:
    print(e)

try:
    db1 = client["newTotalPnl"]
    collec1 = f"newTotalPnl_{date}"
    db1.create_collection(collec1)
    print("newTotalPnl is created")

except Exception as e:
    print(e)

def connect(SymbolList):
    toSend = {}
    print('symList: ', SymbolList)
    sock = socket.socket()
    port = 50122
    sock.connect(('192.168.0.103', port))
    # sock.connect(('localhost', 50000))

    print("Client Connected in Logic")
    # SymbolList=[2885]#,41295,41301,41302]
    toSend['1501'] = SymbolList
    toSend = json.dumps(toSend)
    sock.send(str.encode(toSend))
    field = ['LastTradedPrice']
    field = json.dumps(field)
    _ = sock.recv(1024)
    sock.send(str.encode(field))
    return sock

def symphonyDataConnect(symList):
    sendData = {}
    sendList = []
    for id in idMap.keys():
        sendList.append(int(idMap[id]))
    sock = connect(sendList)
    return sock

def reconnect(sock, data, symbol):
    adderFlag=False
    if symbol:
        if symbol not in symList:
            symList.append(symbol)
            adderFlag=True
            if symbol in stocksMap.keys():
                value = stocksMap[symbol]
                idMap.update({symbol:value})

            if symbol in optionMap.keys():
                # print(optionMap[symbol])
                value = optionMap[symbol]
                idMap.update({symbol:value})


            if symbol in futureMap.keys():
                value = futureMap[symbol]
                idMap.update({symbol:value})

            if symbol in commodityMap.keys():
                value = commodityMap[symbol]
                idMap.update({symbol:value})       

            # newId = sif.connect(symDict={symbol: {'exchangeSegment': 'OPTIDX'}})
            # print(newId)
            # newId = sif.connect(symDict={symbol: {'exchangeSegment': 'FUTSTK'}})
            # newId = sif.connect(symDict={symbol: {'exchangeSegment': 'MCXFO'}})
            # newId = sif.connect(symDict={symbol: {'exchangeSegment': 'EQ'}})
            # newId = sif.connect(symDict={symbol: {'exchangeSegment': 'FUTIDX'}})
            
            # idMap.update(newId)

    if adderFlag:
        if sock:sock.close()

        print('New symbols found, reconnecting....')
        print('New Symlist:', symList)
        sock= symphonyDataConnect(symList)
        d = sock.recv(5120)
        sock.send(str.encode('AWK'))
        data = json.loads(d)
        print ('New data:',data)
        print(idMap)
        return sock,data
    else:
        return sock,data

def getData():
    sock = data = None
                
    while True:
        neworders = db[collec].find()
        for order in neworders:
            if order["quantity"] != 0:

                quan = order["quantity"]
                # print(quan)
                sym = order["symbol"]
                # print(sym)
                sock, data = reconnect(sock, data, sym)
                # print(data)
                # sym = order["symbol"]
                # for i in data.keys():
                ltp = data[idMap[sym]]["LastTradedPrice"]

                sortOfPnl = ltp * int(order["quantity"])
                # print(sortOfPnl)
                # print(order["buy_traded"])
                # print(order["sell_traded"])
                unRealisedPnl = float(order["sell_traded"]) - float(order["buy_traded"]) + sortOfPnl
            else:
                unRealisedPnl = order["sell_traded"] - order["buy_traded"]

            post = {"algoname": order["algoName"], "clientID": order["clientID"], "symbol": order["symbol"], "unRealisedPnl": round(unRealisedPnl)}

            match = db1[collec1].find_one({"$and": [{"algoname": order["algoName"]}, {"clientID": order["clientID"]}, {"symbol": order["symbol"]}]})
            if match:
                print("unRealisedPnl", unRealisedPnl)
                post.update({"unRealisedPnl": round(unRealisedPnl,2)})
                db1[collec1].update({"_id": match["_id"]}, {"$set": post})

            else:
                db1[collec1].insert_one(post)

        

    
    # sock,data = reconnect(sock,data,'BANKNIFTY09JAN2031400PE')
    # sock, data = self.reconnect(sock, data, 'BANKNIFTY09JAN2031500CE')
    # while True:

        if sock:
            d = sock.recv(5120)
            data = json.loads(d)
            sock.send(str.encode('AWK'))
        # print(data)
        # time.sleep(10)

if __name__ == '__main__':
    getData()
