from pymongo import MongoClient
import datetime
import time


# print(dir(db))
# db.create_collection("xyz")

# post = {
#                 "algoName": 'algodemo',
# 				"symbol": 'data6',
# 				"quantity": 34,
# 				"buy_sell": 'SELL',
# }

def savedata(post,date):
    try:
        client = MongoClient()
        db = client['Cumulative_symphonyorder']
        collec = f"cumulative_{date}"
        db.create_collection(collec)
        print(f"Created New Collection '{collec}'")

    except Exception:
        match = db[collec].find_one({ "$and" : [{"algoName":post['algoName']}, {"symbol":post['symbol']},{"clientID":post['clientID']}] })
        if match and post["orderStatus"] == "Filled":
            if post["buy_sell"] == "BUY":
                quantity = match["quantity"]+post['quantity']
                db[collec].update({'_id': match['_id']}, {"$set": {"quantity":quantity, "buy_sell":post["buy_sell"], "time_stamp":post["time_stamp"]}})
                print("BUY REQUEST: ",match)
            if post["buy_sell"] == "SELL":
                quantity = match["quantity"]-post['quantity']
                db[collec].update({'_id': match['_id']}, {"$set": {"quantity":quantity, "buy_sell":post["buy_sell"], "time_stamp":post["time_stamp"]}})
                print("SELL REQUEST: ",match)
            return 0

    if post["buy_sell"] == "BUY" and post["orderStatus"] == "Filled" :
        db[collec].insert(post)
        # print("BUY REQUEST: Quantities Added")
    if post["buy_sell"] == "SELL" and post["orderStatus"] == "Filled":
        quantity = -(post["quantity"])
        post.update({"quantity":quantity})
        # print("SELL REQUEST: Quantities Deducted")
        db[collec].insert(post)
    # print("New Order inserted")
        
# savedata(post)