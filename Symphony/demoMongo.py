from pymongo import MongoClient
import datetime
import time


def savedata(post,date):
    try:
        client = MongoClient()
        db = client['Cumulative_symphonyorder']
        collec = f"cumulative_{date}"
        db.create_collection(collec)
        print(f"Created New Collection '{collec}'")

    except Exception:
        match = db[collec].find_one({ "$and" : [{"algoName":post['algoName']}, {"symbol":post['symbol']},{"clientID":post['clientID']}] })
        # print(match)
        if match and post["orderStatus"] == "Filled":
            OATD = float(post['OrderAverageTradedPrice'])
            quantity = post['quantity']
            if post["buy_sell"] == "BUY":
                new_quantity = match["quantity"]+quantity
                buy_traded = abs(match["buy_traded"]+OATD*quantity)
                new_updation = {"quantity":new_quantity,
                                "buy_sell":post["buy_sell"],
                                "buy_traded": buy_traded,
                                "time_stamp":post["time_stamp"]}
                if new_quantity == 0:
                    pnl = round(match["sell_traded"]-buy_traded,3)
                    new_updation.update({"total_pnl": pnl})
                
                db[collec].update({'_id': match['_id']}, {"$set": new_updation})
                # print("BUY REQUEST: ",match)
            
            if post["buy_sell"] == "SELL":
                new_quantity = match["quantity"]-quantity
                sell_traded = abs(match["sell_traded"])+OATD*quantity
                new_updation = {"quantity":new_quantity,
                                "buy_sell":post["buy_sell"],
                                "sell_traded": sell_traded,
                                "time_stamp":post["time_stamp"]}
                
                if new_quantity == 0:
                    pnl = round(sell_traded-match["buy_traded"],3)
                    new_updation.update({"total_pnl": pnl})
                db[collec].update({'_id': match['_id']}, {"$set": new_updation})
                # print("SELL REQUEST: ",match)  
            
            return 0

    if post["buy_sell"] == "BUY" and post["orderStatus"] == "Filled" :
        OATD = float(post['OrderAverageTradedPrice'])
        post['buy_traded'] = abs(OATD*post['quantity'])
        post['sell_traded'] = 0
        post['total_pnl'] = 0
        print(post)
        db[collec].insert(post)
        print("BUY REQUEST: Quantities Added")
    if post["buy_sell"] == "SELL" and post["orderStatus"] == "Filled":
        OATD = float(post['OrderAverageTradedPrice'])
        post['sell_traded'] = abs(OATD * post['quantity'])
        post['buy_traded'] = 0
        post['total_pnl'] = 0
        quantity = -(post["quantity"])
        post.update({"quantity":quantity})
        # print(post)
        # print("SELL REQUEST: Quantities Deducted")
        db[collec].insert(post)
    # print("New Order inserted")
        
# savedata(post)
