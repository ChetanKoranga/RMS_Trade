from pymongo import MongoClient

connection = MongoClient('localhost', 27017)
# db = connection['GUI']
# collec = f'GUI_{date}'
db = connection['Client_Strategy_Status']
collec = 'Client_Strategy_Status'


class mainfunc:
    def mainoff(self):
        match = db[collec].find({"Start_Stop": {"$eq": "START"}})
        for i in match:
            db[collec].update_one({'_id': i['_id']}, {
                                  "$set": {"Start_Stop": "WAIT"}})

        alloff = db[collec].find()
        for i in alloff:
            db[collec].update_one({'_id': i['_id']}, {"$set": {"main": "OFF"}})

    def mainon(self):
        match = db[collec].find({"Start_Stop": {"$eq": "WAIT"}})
        for i in match:
            db[collec].update_one({'_id': i['_id']}, {
                                  "$set": {"Start_Stop": "START"}})

        allon = db[collec].find()
        for i in allon:
            db[collec].update_one({'_id': i['_id']}, {"$set": {"main": "ON"}})
