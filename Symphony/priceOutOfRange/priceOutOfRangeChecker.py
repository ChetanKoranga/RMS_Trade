import json
import ast
import pymongo
from pymongo import MongoClient
import datetime 
import time
import csv
import symphonyIdFetcher as sif
import OrderManagementSystem

omObj = OrderManagementSystem.OrderSystem()
date = datetime.date.today()
connection=MongoClient()
resp_db = f'order_log_raw_{date}'
final_response = connection.final_response # final database for visualization in table
collec=f'orders_{date}'
responsedb_collec = 'order_log_raw'
final_response_collec='final_response_'+str(date)
# final_response.create_collection(final_response_collec)

# try:
# 	final_response.create_collection('final_response_'+str(date))
# except Exception as e:
# 	print(e)
# 	pass

raw_dict = {}
raw_response_dict = {}
old_value_count = final_response[final_response_collec].count()

algoTOCheck = ['Straddle 1.5:1 AD', 'Straddle Write 4x', 'RMS']
idMap = {}
hedgeFlag = True
hedgeMap = {}
delKeys = []
while True:
	time.sleep(0.1)
	orderid_list = []
	newvalue_count = final_response[final_response_collec].count()
	if old_value_count < newvalue_count :
		new_data = newvalue_count-old_value_count
		new_data_value = final_response[final_response_collec].find().sort([('_id', -1)]).limit(new_data)
		print('Reading new lines:', new_data_value)
		old_value_count = newvalue_count

		for order in new_data_value:
			print(order)
			if order['algoname'] in algoTOCheck:
				if order['buy_sell'] == 'BUY':
					if order['orderStatus'] == 'Cancelled':
						cancelledSym = order['symbol']
						if cancelledSym[-2:] == 'CE':
							hedgeSymbol = cancelledSym[:-7] + str(int(cancelledSym[-7:-2])-100) + 'CE'
							print('hedgeSymbol:', hedgeSymbol)
							newId = sif.connect(symDict={hedgeSymbol:{'exchangeSegment':'OPTIDX'},
												cancelledSym:{'exchangeSegment':'OPTIDX'} })
							idMap.update(newId)
						elif cancelledSym[-2:] == 'PE':
							hedgeSymbol = cancelledSym[:-7] + str(
								int(cancelledSym[-7:-2]) + 100) + 'PE'
							print('hedgeSymbol:', hedgeSymbol)
							newId = sif.connect(symDict={hedgeSymbol: 'OPTIDX',
														 cancelledSym: 'OPTIDX'})
							idMap.update(newId)
						print ('Placing hedge order...')
						omObj.place_order('NSEFO', idMap[hedgeSymbol],'MIS',
										  'MARKET','BUY',order['quantity'])
						hedgeMap[round(time.time())] = {'cancelledSym':cancelledSym,
														'quantity':order['quantity'],
														'hedgeSym':hedgeSymbol,
														'placeTime':time.time(),
														'orderCount':0}
			if hedgeMap:
				print ('Checking hedge sym status...')
				print(idMap)
				for symbol in hedgeMap.keys():
					if (time.time() - (hedgeMap[symbol]['placeTime']) >=0.2) and hedgeMap[symbol]['orderCount'] == 0:
						omObj.place_order('NSEFO', idMap[hedgeMap[symbol]['cancelledSym']], 'MIS',
										  'MARKET', 'BUY', hedgeMap[symbol]['quantity'])
						hedgeMap[symbol]['orderCount']+=1
						hedgeMap[symbol]['placeTime'] = time.time()

					elif hedgeMap[symbol]['orderCount']>0:
						if order['algoname'] == 'RMS':
							if order['symbol'] == hedgeMap[symbol]['cancelledSym'] and order['quantity'] == hedgeMap[symbol]['quantity']:
								if order['orderStatus'] == 'Cancelled':
									print('Place order for symbol')
									omObj.place_order('NSEFO', idMap[hedgeMap[symbol]['cancelledSym']], 'MIS',
													  'MARKET', 'BUY', hedgeMap[symbol]['quantity'])
									hedgeMap[symbol]['orderCount'] += 1

								elif order['orderStatus'] == 'Filled':
									omObj.place_order('NSEFO', idMap[hedgeMap[symbol]['hedgeSym']],
													  'MIS','MARKET', 'BUY',
													  hedgeMap[symbol]['quantity'])
									delKeys.append(symbol)


	if delKeys:
		for key in delKeys:
			del exitMap[key]
		delKeys = []