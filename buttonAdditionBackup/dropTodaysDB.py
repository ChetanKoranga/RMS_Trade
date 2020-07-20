from pymongo import MongoClient
import datetime


connection = MongoClient()
date = datetime.datetime.today().date()
# print(f'final_response_{date}')
cumulative_db = connection.Cumulative_symphonyorder[f'cumulative_{date}']
finalresponse_db = connection.final_response[f'final_response_{date}']
finalpnl_db = connection.finalpnl[f'finalpnl_{date}']
clientWiseTotalPnl_db = connection.clientWiseTotalPnl[f'clientWiseTotalPnl_{date}']
client_order_log_db = connection.client_order_log[f'client_orders_{date}']
newTotalPnl_db = connection.newTotalPnl[f'newTotalPnl_{date}']
order_log_raw_db = connection[f'order_log_raw_{date}']['order_log_raw']
symphonyorder_filtered_db = connection.symphonyorder_filtered[f'neworders_{date}']
symphonyorder_netquantity_db = connection.symphonyorder_netquantity[
    f'symphonyorder_netquantity_{date}']
symphonyorder_raw_db = connection.symphonyorder_raw[f'orders_{date}']

dbs = [cumulative_db, finalresponse_db, finalpnl_db, clientWiseTotalPnl_db, client_order_log_db, newTotalPnl_db,
       order_log_raw_db, symphonyorder_filtered_db, symphonyorder_netquantity_db, symphonyorder_raw_db]

for db in dbs:
    print(db)
    print("DELETED")
    db.drop()

print("DBs deleted successfully...")

# def dropcollection():
#     d.COLLECTION_NAME.drop()
