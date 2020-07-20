from pymongo import MongoClient
import datetime
from time import sleep


def save_pnl():
    date = datetime.date.today()
    new_collec = f'finalpnl_{date}'
    try:
        client = MongoClient()
        db = client['newTotalPnl']
        collec = f"newTotalPnl_{date}"
        db.create_collection(collec)
        print(f"Created New Collection '{collec}'")
        # while True:
        # sleep(1)

    except Exception as e:
        print(e)

    try:
        new_client = MongoClient()
        finalpnl_db = new_client['finalpnl']
        finalpnl_db[new_collec].drop()
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

    finally:
        while True:
            # sleep(1)
            present_documents = []
            documents = db[collec].find()
            # for i in documents:
            #     print(i)
            for feed in documents:
                common = feed["clientID"]+feed["algoname"]
                if common in present_documents:
                    continue
                else:
                    present_documents.append(common)
                    # print(common)
                    match = db[collec].find(
                        {"$and": [{"algoname": feed['algoname']}, {"clientID": feed['clientID']}]})
                    # print(match)
                    # if match:
                    pnl = 0
                    for i in match:
                        # print(i)
                        pnl += round(i["unRealisedPnl"], 2)
                        # print("TOTAL PNL: ",pnl,"\n")
                    match = db[collec].find(
                        {"$and": [{"algoname": feed['algoname']}, {"clientID": feed['clientID']}]})
                    for j in match:
                        # j["strategywise_pnl"] = pnl
                        # print(j)
                        db[collec].update({'_id': j['_id']}, {
                                          "$set": {"strategywise_pnl": round(pnl, 2)}})

save_pnl()
