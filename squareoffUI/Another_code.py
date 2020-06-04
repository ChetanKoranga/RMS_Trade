from pymongo import MongoClient
import time
import datetime

date = datetime.date.today()
client = MongoClient()

try:
    db = client["Client_Strategy_Status"]
    collec = f"Client_Strategy_Status"
    db.create_collection(collec)
    print("GUI database created")

except Exception as e:
    print(e)

AlgoName = str(input("Enter AlgoName: "))
ClientID = str(input("Enter ClientID: "))

# orders = db[collec].find()
# for order in orders:
#     # print(order)
match = db[collec].find_one({"$and": [{"AlgoName": AlgoName, "ClientID": ClientID}]})

if match:
    print(match["Start_Stop"])
    print(type(match["Start_Stop"]))

else:
    print("does not exists")    
