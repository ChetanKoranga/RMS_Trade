import sys
import datetime
from pymongo import MongoClient
import orderSlicer
from multiprocessing import Process
import csv


class sqoff:
    date = datetime.date.today()

    def squareoff(self, strategyName, clientID):
        collec = f'cumulative_{self.date}'
        print("yay")
        try:
            connection = MongoClient('localhost', 27017)
            cumulative_db = connection.Cumulative_symphonyorder
            cumulative_collection = cumulative_db[collec]
        except:
            print("Could not connect to database. Please check your connection.")

        if strategyName == "All" and clientID == "All":
            print(strategyName, "========", clientID)
            documents = cumulative_collection.find()
        elif strategyName == "All":
            print(strategyName, "========", clientID)
            documents = cumulative_collection.find({'clientID': clientID})
        elif clientID == "All":
            print(strategyName, "========", clientID)
            documents = cumulative_collection.find({'algoName': strategyName})
        else:
            print(strategyName, "========", clientID)
            documents = cumulative_collection.find(
                {"$and": [{"algoName": strategyName}, {"clientID": clientID}]})

        # order = orderManagement.OrderSystem()
        # order = orderManagement.OrderSystem2()
        obj = orderSlicer.OrderSystem()
        for doc in documents:
            # print("DOCS=====",doc)
            exchangeSegment = doc["exchangeSegment"]
            exchangeInstrumentID = doc["exchangeInstrumentID"]
            productType = doc["productType"]
            orderType = 'MARKET'  # doc["orderType"]
            orderQuantity = doc["quantity"]
            if orderQuantity < 0:
                orderSide = "BUY"
            else:
                orderSide = "SELL"

            algoName = doc["algoName"]
            clientID = doc['clientID']
            symbol = doc["symbol"]
            try:
                with open(rf'C:\Users\Mudraksh_Server1\Desktop\ServerCodes\Symphony Order Server Dealer 2.0\Allowed algos\\{algoName}.txt') as file:
                    otp = file.read()
                    # print(otp)
            except Exception as e:
                pass
            if symbol.startswith("BANKNIFTY") and orderQuantity != 0:
                if 'FUT' not in symbol:
                    # if abs(orderQuantity) > 60:
                    p1 = Process(target=obj.placeSliceOrder, args=(
                        exchangeSegment, exchangeInstrumentID, productType, orderType, orderSide, abs(
                            orderQuantity), algoName,
                        clientID, 200,
                        0.1, otp)).start()
                    # else:
                    #     order.place_order(exchangeSegment, exchangeInstrumentID, productType, orderType, orderSide,
                    #                       abs(orderQuantity), algoName, clientID)
                else:
                    p1 = Process(target=obj.placeSliceOrder, args=(
                        exchangeSegment, exchangeInstrumentID, productType, orderType, orderSide, abs(
                            orderQuantity), algoName,
                        clientID, 100,
                        0.1, otp)).start()
            elif symbol.startswith("NIFTY") and orderQuantity != 0:
                # if abs(orderQuantity) > 225:
                p1 = Process(target=obj.placeSliceOrder, args=(
                    exchangeSegment, exchangeInstrumentID, productType, orderType, orderSide, abs(
                        orderQuantity), algoName,
                    clientID, 750,
                    0.2, otp)).start()
                # else:
                #     order.place_order(exchangeSegment, exchangeInstrumentID, productType, orderType, orderSide,
                #                       abs(orderQuantity), algoName, clientID)
            # elif orderQuantity != 0:
            #     order.place_order(exchangeSegment, exchangeInstrumentID, productType,
            #                       orderType, orderSide, abs(orderQuantity), algoName, clientID)
            # if orderQuantity != 0:
            #     order.place_order(exchangeSegment,exchangeInstrumentID,productType,orderType,orderSide,orderQuantity,algoName,clientID)
            # ,exchangeSegment,exchangeInstrumentID,
                # 	   productType,orderType,orderSide,orderQuantity, algoName
        print("SquareOff Successfull.")

    def squareoff_all(self):
        print("heyyyyy")
        collec = f'cumulative_{self.date}'

        try:
            connection = MongoClient('localhost', 27017)
            cumulative_db = connection.Cumulative_symphonyorder
            cumulative_collection = cumulative_db[collec]
        except:
            print("Could not connect to database. Please check your connection.")

        documents = cumulative_collection.find()
        # order = orderManagement.OrderSystem()
        # order = orderManagement.OrderSystem2()
        obj = orderSlicer.OrderSystem()
        for doc in documents:
            # if doc['algoName'] != '1000 EMA Overnight' and doc['algoName'] != 'SpreadSell':
            if 'Overnight' not in doc['algoName']:
                exchangeSegment = doc["exchangeSegment"]
                exchangeInstrumentID = doc["exchangeInstrumentID"]
                productType = doc["productType"]
                orderType = 'MARKET'  # doc["orderType"]

                orderQuantity = doc["quantity"]
                if orderQuantity < 0:
                    orderSide = "BUY"
                else:
                    orderSide = "SELL"

                algoName = doc["algoName"]
                clientID = doc["clientID"]
                symbol = doc["symbol"]
                print("SYMBOL ======", symbol)

                try:
                    with open(rf'C:\Users\Mudraksh_Server1\Desktop\ServerCodes\Symphony Order Server Dealer 2.0\Allowed algos\\{algoName}.txt') as file:
                        otp = file.read()
                        # print(otp)
                except Exception as e:
                    pass

                if symbol.startswith("BANKNIFTY") and orderQuantity != 0:
                    print("HEY BANK")
                    if 'FUT' not in symbol:
                        # if abs(orderQuantity) > 60:
                        p1 = Process(target=obj.placeSliceOrder, args=(
                            exchangeSegment, exchangeInstrumentID, productType, orderType, orderSide, abs(
                                orderQuantity), algoName,
                            clientID, 200,
                            0.1, otp)).start()
                        # else:
                        #     order.place_order(exchangeSegment, exchangeInstrumentID, productType, orderType, orderSide,
                        #                       abs(orderQuantity), algoName, clientID)
                    else:
                        p1 = Process(target=obj.placeSliceOrder, args=(
                            exchangeSegment, exchangeInstrumentID, productType, orderType, orderSide, abs(
                                orderQuantity), algoName,
                            clientID, 100,
                            0.1, otp)).start()

                elif symbol.startswith("NIFTY") and orderQuantity != 0:
                    print("HEY NIF")
                    # if abs(orderQuantity) > 225:
                    p1 = Process(target=obj.placeSliceOrder, args=(
                        exchangeSegment, exchangeInstrumentID, productType, orderType, orderSide, abs(
                            orderQuantity), algoName,
                        clientID, 750,
                        0.2, otp)).start()
                # else:
                #     order.place_order(exchangeSegment, exchangeInstrumentID, productType, orderType, orderSide,
                #                       abs(orderQuantity), algoName, clientID)
            # elif orderQuantity != 0:
            #     print("HEY OTHER")
            #     order.place_order(exchangeSegment, exchangeInstrumentID, productType, orderType, orderSide,
            #                       abs(orderQuantity), algoName, clientID)

            # if orderQuantity != 0:
            #     order.place_order(exchangeSegment,exchangeInstrumentID,productType,orderType,orderSide,abs(orderQuantity),algoName,clientID)
            # ,exchangeSegment,exchangeInstrumentID,
                # 	   productType,orderType,orderSide,orderQuantity, algoName
        print("SquareOff Successfull.")


