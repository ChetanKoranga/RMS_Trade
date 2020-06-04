from pymongo import MongoClient
import datetime
import time


# list = [{clientID:,symbol:,quantity},{clientID:,symbol:,quantity},{clientID:,symbol:,quantity}]

def savedata(post, date):
    # print(post)
    try:
        client = MongoClient()
        db = client['symphonyorder_netquantity']
        collec = f"symphonyorder_netquantity_{date}"
        db.create_collection(collec)
        print(f"Created New Collection '{collec}'")
        db[collec].insert(post)
        # print(post)

    except Exception:
        match = db[collec].find_one({"$and": [{"symbol": post['symbol']},
                                              {"clientID": post['clientID']}]})
        # print(match)

        if match:
            # print(match)
            quantity = post['quantity']
            #new_quantity = quantity
            # print(new_quantity)
            # if quantity != 0:
            new_quantity = match["quantity"]+quantity
            print(new_quantity)
            db[collec].update({'_id': match['_id']}, {
                              "$set": {"quantity": new_quantity}})

        else:
            # print(post['quantity'])
            db[collec].insert(post)
            print("new Quantities Added")
