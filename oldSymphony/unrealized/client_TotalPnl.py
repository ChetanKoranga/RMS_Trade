import pymongo
from pymongo import MongoClient
import datetime
import time
from flask import Flask
from flask_socketio import SocketIO
import socket

date = datetime.date.today()

client = MongoClient()

try:
    db = client["finalpnl"]
    collec = f"finalpnl_{date}"
    db.create_collection(collec)
    print("finalpnl is created")

except Exception as e:
    print(e)    

try:
    db1 = client["clientWiseTotalPnl"]
    collec1 = f"clientWiseTotalPnl_{date}"
    db1.create_collection(collec1)
    print("clientWiseTotalPnl is created")

except Exception as e:
    print(e)    


while True:
    orders = db[collec].find()
    for order in orders:
        cID = order["clientID"]
        urPnl = order["strategywise_pnl"]
        
        match = db[collec].find({"clientID": cID})
    
        newUrTotal = 0
        if match:
            for i in match:
                newUrTotal = float(i["strategywise_pnl"]) + newUrTotal
                
            matchInDb1 = db1[collec1].find_one({"clientID": cID})
            post = {"clientID":cID, "unRealized_pnl": newUrTotal}
            if matchInDb1:
                db1[collec1].update({"_id":matchInDb1["_id"]}, {"$set":post})

            else:
                db1[collec1].insert_one(post)


    









