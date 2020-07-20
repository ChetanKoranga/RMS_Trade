from pymongo import MongoClient
import time
import datetime

def alarm_reason(alarm_id,type,file,system,reason):
    date=datetime.date.today()
    time_stamp=str(datetime.datetime.now().time())
    # print(time_stamp)
    post={"alarm id":alarm_id,"time_stamp":time_stamp,"alarm type":type,"file name":file,"system":system,"reason":reason}
    try:
        client = MongoClient(host="192.168.0.103")
        db = client['check_alarm']
        collec = f"check_alarm{date}"
        db.create_collection(collec)
        print("collection created")
        db[collec].insert(post)
    except:
##        match=db[collec].find_one({"alarm id":alarm_id})
##        if match:
##            # print(match)
##            db[collec].update({"_id":match['_id']},{"$set":post})
##        else:
        db[collec].insert(post)

##alarm_reason("id","error","abc","algo","algo open")
##print("done")
