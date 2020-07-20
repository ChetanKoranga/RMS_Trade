from pymongo import MongoClient
import datetime
from time import sleep



date = datetime.date.today()
new_collec = f'finalpnl_{date}'

try:
    client = MongoClient()
    db = client['newTotalPnl']
    collec = f'newTotalPnl_{date}'
    db.create_collection(collec)
    print(f"created new collection '{collec}'")

except Exception as e:
    print(e)

try:
    new_client = MongoClient()
    exitpnl_db = new_client['finalpnl']
    exitpnl_db[new_collec].drop()
    print('finalpnl Collec Deleted')
except:
    pass

try:
    new_client = MongoClient()
    new_db = new_client['finalpnl']
    new_db.create_collection(new_collec)
    print(f"created new collection '{new_collec}'")

except Exception as e:
    print(e)


# algoname_unique = db[collec].find().distinct("algoname")
# print(algoname_unique)

# ClientID_unique = db[collec].find().distinct("clientID")
# print(ClientID_unique)

# l = []
# for x in algoname_unique:
#     for y in ClientID_unique:
#         conca = x + y
#         l.append(conca)       
# print(l)    

while True:
    check = db[collec].find()
    li = []

    for z in check:    
        conca = z["clientID"]+ z["algoname"]
        if conca in li:
            continue
           
        else:
            li.append(conca)
            match = new_db[new_collec].find_one({ "$and" : [{"algoname": z['algoname']},{"clientID": z['clientID']}] })
            if match:
                try:
                    new_db[new_collec].update({'_id' : match['_id']}, {"$set": {"strategywise_pnl": z['strategywise_pnl']}})
                except Exception:
                    print("Waiting for PnL")
                    pass

            else:
                try:
                    post={"algoname":z['algoname'], "clientID":z['clientID'],"strategywise_pnl":z['strategywise_pnl']}
                    new_db[new_collec].insert_one(post)
                except Exception:
                    print("Waiting for PnL")
                    pass

        
        
        
        
        
        
          # check = db[collec].find()
                    # l = []
                    # for x in check:    
                    #     conca = x["clientID"]+ x["algoname"]
                    #     if conca in l:
                    #         continue
                    #     else:
                    #         l.append(conca)
                    #         new_db[new_collec].insert(db[collec].find({},{ "_id": 0, "algoname": 1, "clientID": 1, "strategywise_pnl": 1 }))
