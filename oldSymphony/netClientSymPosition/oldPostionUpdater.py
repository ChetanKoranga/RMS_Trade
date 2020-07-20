from pymongo import MongoClient
import datetime
import pandas as pd

def run():
    lastDay =int(input('Enter days to last working day: '))
    lastWorkingDate = datetime.datetime.today() - datetime.timedelta(days=lastDay)
    lastWorkingDate = lastWorkingDate.date()
    print(lastWorkingDate)
    conn = MongoClient()
    dbName = 'Cumulative_symphonyorder'
    db = conn[dbName]
    lastcollecName = f'cumulative_{lastWorkingDate}'
    lastCollec = db[lastcollecName]
    oldPositionDf = pd.DataFrame(list(lastCollec.find()))
    oldPositionDf = oldPositionDf[oldPositionDf['quantity']!=0]
    today = datetime.date.today()
    todaycollec = f'cumulative_{today}'
    if not oldPositionDf.empty:
        db[todaycollec].insert_many(oldPositionDf.to_dict('records'))

if __name__ == "__main__":
    run()