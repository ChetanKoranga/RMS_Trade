from flask import Flask, render_template, jsonify, request
from flask_restful import Api, Resource
from flask_cors import CORS
from pymongo import MongoClient
import datetime
import json
import random
import csv
from bson import ObjectId

app = Flask(__name__)
api = Api(app)
CORS(app)
date = datetime.date.today()
timestamp = str(datetime.datetime.now().time())
connection = MongoClient('localhost', 27017)
# db = connection['GUI']
# collec = f'GUI_{date}'
db = connection['Client_Strategy_Status']
collec = 'Client_Strategy_Status'
listdb = connection['all_list']
collectionalgo = listdb['algo']
collectionclient = listdb['client']
resp_db = connection['final_response']
resp_collec = resp_db[f"final_response_{date}"]


# x=collection.insert_one({"algoname":"hoooo"})
print(connection.list_database_names())
# collection=listdb["algo"]


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)


monitordb = connection['algo_status']
monitor_collec = f'status_{date}'


def checkPostedData(postedData, method):
    if method == "updatedb":
        if postedData["Algoname"] == "" or postedData["ClientID"] == "" or postedData["Status"] == "" or postedData["losslimit"] == "" or postedData["quantity_multiple"] == "" or postedData["TradeLimitPerDay"] == "" or postedData["QuantityLimitPerTrade"] == "" or postedData["lotSize"] == "" or postedData["sliceSize"] == "" or postedData["waitTime"] == "" or postedData["tradeLimitPerSecond"] == "":
            return 301
        else:
            return 200

    if method == "updatemonitordb":
        if "algoName" not in postedData or "Status" not in postedData:
            return 301
        else:
            return 200

    if method == "updateotpdb":
        if "Algoname" not in postedData or "OTP" not in postedData:
            return 301
        else:
            return 200

    if method == "updatemanualorder":
        if "Algoname" not in postedData or "ClientID" not in postedData or "ExchangeSegment" not in postedData or "Symbol" not in postedData or "OrderSide" not in postedData or "OrderQuantity" not in postedData or "OrderAverageTradedPrice" not in postedData:
            return 301
        else:
            return 200

    # if method == "updatelist":
    #     if "algolist" not in postedData or "clientlist" not in postedData or "action" not in postedData:
    #         return 301
    #     else:
    #         return 200


class updatelist(Resource):
    support_cors = True
    cors_origin = '*'
    cors_headers = 'origin, content-type, x-request-with'
    # @app.route('/listupdate', methods=['GET'])

    def post(self):
        postedData = request.get_json()
        Algolist = postedData["algolist"]

        Action = postedData["action"]
        print(postedData)
        # status = checkPostedData(postedData, "updatelist")
        # if status== 301:
        #     return "Parameter error. Please check the parameters"
        # else:
        if Action == 'add':
            match = collectionalgo.find_one({"value": Algolist})
            if not match:
                if (Algolist != ''):
                    collectionalgo.insert_one(
                        {"key": Algolist, "text": Algolist, "value": Algolist})
                    dict = {"algolist": []}
                    docs = collectionalgo.find()
                    for doc in docs:
                        dict["algolist"].append(doc)
                    return JSONEncoder().encode(dict)

        elif Action == 'remove':
            if (Algolist != ''):
                collectionalgo.delete_one(
                    {"key": Algolist, "text": Algolist, "value": Algolist})
                dict = {"algolist": []}
                docs = collectionalgo.find()
                for doc in docs:
                    dict["algolist"].append(doc)
                return JSONEncoder().encode(dict)


class getalgo(Resource):
    support_cors = True
    cors_origin = '*'
    cors_headers = 'origin,content-type,x-request-with'

    def get(self):
        data = []
        raw = collectionalgo.find()
        for d in raw:
            d["_id"] = JSONEncoder().encode(d["_id"])
            data.append(d)
        return data


class updatedb(Resource):
    support_cors = True
    cors_origin = '*'
    cors_headers = 'origin, content-type, x-request-with'

    def post(self):
        postedData = request.get_json()
        algoname = postedData["Algoname"]
        clientid = postedData["ClientID"]
        start_stop = postedData["Status"]
        loss_limit = postedData["losslimit"]
        multiple_quantity = postedData["quantity_multiple"]
        TradeLimitPerDay = postedData["TradeLimitPerDay"]
        QuantityLimitPerTrade = postedData["QuantityLimitPerTrade"]
        lotSize = postedData["lotSize"]
        sliceSize = postedData["sliceSize"]
        waitTime = postedData["waitTime"]
        tradeLimitPerSecond = postedData["tradeLimitPerSecond"]
        status = checkPostedData(postedData, "updatedb")
        if status == 301:
            return "Parameter error. Please check the parameters"
        else:
            match = db[collec].find_one(
                {"$and": [{"algoname": algoname}, {"ClientID": clientid}]})

            if match:
                db[collec].update_one({'_id': match['_id']}, {
                    "$set": {"Start_Stop": start_stop, "losslimit": loss_limit, "quantity_multiple": multiple_quantity, "TradeLimitPerDay": TradeLimitPerDay, "QuantityLimitPerTrade": QuantityLimitPerTrade, "lotSize": lotSize, "sliceSize": sliceSize, "waitTime": waitTime, "tradeLimitPerSecond": tradeLimitPerSecond}})
            # elif algoname=="ALL"  &&  clientid!="ALL":
            #     for
            #     db[collec].insert_many({

            #     )}

            elif algoname == "All":
                for i in collectionalgo.distinct("value"):
                    if i == "All":
                        continue
                    else:
                        db[collec].insert_one(
                            {"algoname": i, "ClientID": clientid, "Start_Stop": start_stop, "losslimit": loss_limit, "quantity_multiple": multiple_quantity,  "TradeLimitPerDay": TradeLimitPerDay, "QuantityLimitPerTrade": QuantityLimitPerTrade, "lotSize": lotSize, "sliceSize": sliceSize, "waitTime": waitTime, "tradeLimitPerSecond": tradeLimitPerSecond})

            elif clientid == "All":
                for i in collectionclient.distinct("client"):
                    match = db[collec].find_one(
                        {"$and": [{"algoname": algoname}, {"ClientID": i}]})
                    if i == "All":
                        continue
                    elif match:
                        db[collec].update_one({'_id': match['_id']}, {
                                              "$set": {"Start_Stop": start_stop, "losslimit": loss_limit, "quantity_multiple": multiple_quantity, "TradeLimitPerDay": TradeLimitPerDay, "QuantityLimitPerTrade": QuantityLimitPerTrade, "lotSize": lotSize, "sliceSize": sliceSize, "waitTime": waitTime, "tradeLimitPerSecond": tradeLimitPerSecond}})
                    else:
                        db[collec].insert_one(
                            {"algoname": algoname, "ClientID": i, "Start_Stop": start_stop, "losslimit": loss_limit, "quantity_multiple": multiple_quantity, "TradeLimitPerDay": TradeLimitPerDay, "QuantityLimitPerTrade": QuantityLimitPerTrade, "lotSize": lotSize, "sliceSize": sliceSize, "waitTime": waitTime, "tradeLimitPerSecond": tradeLimitPerSecond})

            else:
                db[collec].insert_one({"algoname": algoname,
                                       "ClientID": clientid,
                                       "Start_Stop": start_stop,
                                       "losslimit": loss_limit,
                                       "quantity_multiple": multiple_quantity,
                                       "TradeLimitPerDay": TradeLimitPerDay,
                                       "QuantityLimitPerTrade": QuantityLimitPerTrade,
                                       "lotSize": lotSize,
                                       "sliceSize": sliceSize,
                                       "waitTime": waitTime,
                                       "tradeLimitPerSecond": tradeLimitPerSecond})

            return "ok"


class updatemonitordb(Resource):
    support_cors = True
    cors_origin = '*'
    cors_headers = 'origin, content-type, x-request-with'

    def post(self):
        postedData = request.get_json()
        algoname = postedData["algoName"]
        start_stop = postedData["Status"]
        status = checkPostedData(postedData, "updatemonitordb")
        if status == 301:
            return "Parameter error. Please check the parameters"
        elif status == 200:
            # print(algoname, monitordb, monitor_collec)
            match = monitordb[monitor_collec].find({"Algoname": algoname})
            # print(match)
            if match:
                for m in match:
                    print("Gottcha====", m)
                    updation = monitordb[monitor_collec].update({'_id': m['_id']}, {
                        "$set": {"Status": start_stop}})
                    print(updation)
                return "done"
            else:
                return "nothing found"


class updateotpdb(Resource):
    support_cors = True
    cors_origin = '*'
    cors_headers = 'origin, content-type, x-request-with'

    def post(self):
        postedData = request.get_json()
        algoname = postedData["Algoname"]
        otp = postedData["OTP"]
        status = checkPostedData(postedData, "updateotpdb")
        if status == 301:
            return "Parameter error. Please check the parameters"
        elif status == 200:
            filePath = r'C:\Users\Mudraksh_Server1\Desktop\ServerCodes\Symphony Order Server Dealer 2.0\Allowed algos/'
            f = open(filePath+algoname+".txt", 'w')
            f.write(otp)
            f.close()


class updatemanualorder(Resource):
    support_cors = True
    cors_origin = '*'
    cors_headers = 'origin, content-type, x-request-with'

    def post(self):
        postedData = request.get_json()
        Algoname = postedData["Algoname"]
        ClientID = postedData["ClientID"]
        ExchangeSegment = postedData["ExchangeSegment"]
        Symbol = postedData["Symbol"]
        OrderSide = postedData["OrderSide"].upper()
        OrderQuantity = postedData["OrderQuantity"]
        OrderAverageTradedPrice = postedData["OrderAverageTradedPrice"]
        status = checkPostedData(postedData, "updatemanualorder")
        if status == 301:
            return "Parameter error. Please check the parameters"
        elif status == 200:
            if Symbol in futureMap.keys():
                exchangeinstrumentID = futureMap[Symbol]

            elif Symbol in optionMap.keys():
                exchangeinstrumentID = optionMap[Symbol]

            elif Symbol in commodityMap.keys():
                exchangeinstrumentID = commodityMap[Symbol]

            elif Symbol in stocksMap.keys():
                exchangeinstrumentID = stocksMap[Symbol]

            else:
                exchangeinstrumentID = Symbol

            if ClientID == "All":
                for i in collectionclient.distinct("client"):
                    if i == "All":
                        continue
                    else:
                        resp_collec.insert_one({
                            "quantity": OrderQuantity,
                            "algoname": Algoname,
                            "symbol": Symbol,
                            "exchangeInstrumentID": exchangeinstrumentID,
                            "exchangeSegment": ExchangeSegment,
                            "buy_sell": OrderSide,
                            "time_stamp": timestamp,
                            "productType": "MIS",
                            "orderStatus": "Filled",
                            "cancelrejectreason": "",
                            "OrderAverageTradedPrice": OrderAverageTradedPrice,
                            "clientID": i
                        })

            else:
                resp_collec.insert_one({
                    "quantity": OrderQuantity,
                    "algoname": Algoname,
                    "symbol": Symbol,
                    "exchangeInstrumentID": exchangeinstrumentID,
                    "exchangeSegment": ExchangeSegment,
                    "buy_sell": OrderSide,
                    "time_stamp": timestamp,
                    "productType": "MIS",
                    "orderStatus": "Filled",
                    "cancelrejectreason": "",
                    "OrderAverageTradedPrice": OrderAverageTradedPrice,
                    "clientID": ClientID
                })


class CsvToDict:
    optionIDSymname = {}
    reader = csv.reader(open('OptionIds.txt', 'r'))
    for row in reader:
        k, v1 = row
        optionIDSymname[v1] = k

    futIDSymname = {}
    reader = csv.reader(open('FuturesIds.txt', 'r'))
    for row in reader:
        k, v1 = row
        futIDSymname[v1] = k

    commodityIDSymname = {}
    reader = csv.reader(open('MCXIds.txt', 'r'))
    for row in reader:
        k, v1 = row
        commodityIDSymname[v1] = k

    stocksIDSymname = {}
    reader = csv.reader(open('stocksIds.txt', 'r'))
    for row in reader:
        k, v1 = row
        stocksIDSymname[v1] = k


obj = CsvToDict()
stocksMap = obj.stocksIDSymname
optionMap = obj.optionIDSymname
futureMap = obj.futIDSymname
commodityMap = obj.commodityIDSymname


api.add_resource(updatedb, "/updatedb")
api.add_resource(updatemonitordb, "/monitorupdate")
api.add_resource(updatelist, "/listupdate")
api.add_resource(getalgo, "/getalgo")
api.add_resource(updateotpdb, "/updateotpdb")
api.add_resource(updatemanualorder, "/updatemanualorder")

app.run(debug=True)
