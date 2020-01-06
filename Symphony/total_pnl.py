from pymongo import MongoClient
import datetime
from time import sleep


def save_pnl():
    date = datetime.date.today()
    new_collec = f'exitpnl_{date}'
    try:
        client = MongoClient()
        db = client['Cumulative_symphonyorder']
        collec = f"cumulative_{date}"
        db.create_collection(collec)
        print(f"Created New Collection '{collec}'")
        # while True:
            # sleep(1)

    except Exception as e:
        print(e)

    try:
        new_client = MongoClient()
        exitpnl_db = new_client['exitpnl']
        exitpnl_db[new_collec].drop()
        print('exitpnl Collec Deleted')
    except:
        pass

    try:
        new_client = MongoClient()
        new_db = new_client['exitpnl']
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
                common = feed["clientID"]+feed["algoName"]
                if common in present_documents:
                    continue
                else:
                    present_documents.append(common)
                    # print(common)
                    match = db[collec].find({ "$and" : [{"algoName":feed['algoName']},{"clientID":feed['clientID']}] })
                        # print(match)
                    # if match:    
                    pnl = 0
                    for i in match:
                        # print(i)
                        pnl += i["total_pnl"]
                        # print("TOTAL PNL: ",pnl,"\n")
                    match = db[collec].find({ "$and" : [{"algoName":feed['algoName']},{"clientID":feed['clientID']}] })
                    for j in match:
                        # j["strategywise_pnl"] = pnl 
                        # print(j)
                        db[collec].update({'_id': j['_id']}, {"$set": {"strategywise_pnl":pnl}})





              # get strategywise pnl to exitpnl database
              #   check = db[collec].find()
              #   li = []
              #
              #   for z in check:
              #       conca = z["clientID"] + z["algoName"]
              #       if conca in li:
              #           continue
              #
              #       else:
              #           li.append(conca)
              #           match = new_db[new_collec].find_one(
              #               {"$and": [{"algoName": z['algoName']}, {"clientID": z['clientID']}]})
              #           if match:
              #               new_db[new_collec].update({'_id': match['_id']},
              #                                         {"$set": {"strategywise_pnl": z['strategywise_pnl']}})
              #
              #           else:
              #               post = {"algoName": z['algoName'], "clientID": z['clientID'],
              #                       "strategywise_pnl": z['strategywise_pnl']}
              #
              #               new_db[new_collec].insert_one(post)

        
        
save_pnl()