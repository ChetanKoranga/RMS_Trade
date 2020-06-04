import json
import ast
import pymongo
from pymongo import MongoClient
import datetime 
import time
import csv

date = datetime.date.today()

# final_responses='final_response_'+str(date)

connection=MongoClient()
resp_db = f'order_log_raw_{date}'
nsecm_final_response = connection.nsecm_final_response # final database for visualization in table
all_final_response = connection.all_final_response

raw_db = connection.symphonyorder_raw   		# raw database of requested orders
responsedb = connection[resp_db]		# database having broker response

collec=f'orders_{date}'
responsedb_collec = 'order_log_raw'
nsecm_collec = 'nsecm_response_'+str(date)
all_collec = 'all_response_'+str(date)
# nsecm_final_response.create_collection(nsecm_collec)


try:
	nsecm_final_response.create_collection(nsecm_collec)
	all_final_response.create_collection(all_collec)
except Exception as e:
	print(e)
	pass

raw_dict = {}
raw_response_dict = {}
old_value_count = raw_db[collec].count()
oldresponse_count = responsedb[responsedb_collec].count()




class CsvToDict:

    optionIDSymname={}
    reader = csv.reader(open(r'C:\Users\Mudraksh_Server1\Desktop\ServerCodes\test\Symphony Order Server\OptionIds.txt', 'r'))
    for row in reader:
        v1,k=row
        optionIDSymname[v1]=k

    futIDSymname = {}
    reader = csv.reader(open(r'C:\Users\Mudraksh_Server1\Desktop\ServerCodes\test\Symphony Order Server\FuturesIds.txt', 'r'))
    for row in reader:
        v1, k = row
        futIDSymname[v1] = k

    commodityIDSymname = {}
    reader = csv.reader(open(r'C:\Users\Mudraksh_Server1\Desktop\ServerCodes\test\Symphony Order Server\MCXIds.txt', 'r'))
    for row in reader:
        v1, k = row
        commodityIDSymname[v1] = k

    stocksIDSymname = {}
    reader = csv.reader(open(r'C:\Users\Mudraksh_Server1\Desktop\ServerCodes\test\Symphony Order Server\stocksIds.txt', 'r'))
    for row in reader:
        v1, k = row
        stocksIDSymname[v1] = k

obj = CsvToDict()
stocksMap= obj.stocksIDSymname
optionMap = obj.optionIDSymname
futureMap= obj.futIDSymname
commodityMap=obj.commodityIDSymname



while True:
	orderid_list = []
	time.sleep(1)
	newvalue_count = raw_db[collec].count()
	# print("New val:",newvalue_count)
	if old_value_count < newvalue_count :
		new_data = newvalue_count-old_value_count
		# print('new data',new_data)
		new_data_value = raw_db[collec].find().sort([('_id', -1)]).limit(new_data)
		# print('asdf',new_data_value)
		old_value_count = newvalue_count

		for order in new_data_value:

			print('ORDERS:  ',order)
			# extract algoname  frontend:algoname,symbol,quantity(raw_databae),timestamp,buy_sell,orderstatus,rejected_quantity
			identifier = order['orderUniqueIdentifier']
			quantity = order['orderQuantity']
			algoname = order['algoName']
			instrumentID = order['exchangeInstrumentID']
			orderside = order['orderSide']

			post = {
				identifier: {
					'quantity': quantity,
					'algoname': algoname,
					'instrumentID': instrumentID,
					'orderside' : orderside
				}
			}
			raw_dict.update(post)
		# print('RAWDICT: ',raw_dict)

		# symbol:mapping exchangeinstumentid socketflask
	if raw_dict:
		newresponse_count = responsedb[responsedb_collec].count()
		print('NEW RESPONSE:  ',newresponse_count)
		if newresponse_count > oldresponse_count:
			new_responsedata = newresponse_count-oldresponse_count
			responseDataValue = responsedb[responsedb_collec].find().sort([('_id', -1)]).limit(new_responsedata)
			for response in responseDataValue:
				timestamp = str(datetime.datetime.now().time())
				orderuniqueidentifier = response['OrderUniqueIdentifier']
				orderstatus = response['OrderStatus']
				cancelrejectreason = response['CancelRejectReason']
				# quantitybroker = responseDataValue['OrderQuantity']
				rejectedquantity = response['CumulativeQuantity']
				OrderAverageTradedPrice = response['OrderAverageTradedPrice']
				ExchangeSegment = response['ExchangeSegment']

				response_post = {
					orderuniqueidentifier: {
						'timestamp': str(timestamp),
						'orderstatus': orderstatus,
						'cancelrejectreason': cancelrejectreason,
						# 'rejectedquantity': rejectedquantity,
						'OrderAverageTradedPrice' : OrderAverageTradedPrice,
						'ExchangeSegment' : ExchangeSegment
					}
				}
				# print('RESPOST: ',response_post)
				raw_response_dict.update(response_post)


				for orderid in raw_dict.keys():
					# print('OrderID:', orderid)
					# print('Response Dict:', raw_response_dict)
					if str(orderid) in raw_response_dict.keys():
						print('ID found')
						print('OrderStatus:', raw_response_dict[orderid]['orderstatus'])
						if raw_response_dict[orderid]['orderstatus'] == "Filled" or raw_response_dict[orderid]['orderstatus'] == "Rejected":
							print('checked status')
							symbolID = str(raw_dict[orderid]['instrumentID'])
							if symbolID in futureMap.keys():
									symbol = futureMap[symbolID]

							elif symbolID in  optionMap.keys():
									symbol = optionMap[symbolID]

							elif symbolID in commodityMap.keys():
									symbol = commodityMap[symbolID]

							elif symbolID in stocksMap.keys():
									symbol = stocksMap[symbolID]
							else:
								symbol = symbolID

							if raw_response_dict[orderid]['ExchangeSegment'] != 'NSECM':
								final_post = {
									'quantity': raw_dict[orderid]['quantity'],
									'algoname': raw_dict[orderid]['algoname'],
									'instrumentID': symbol,
									'orderside' : raw_dict[orderid]['orderside'],
									'timestamp': raw_response_dict[orderid]['timestamp'],
									'orderstatus': raw_response_dict[orderid]['orderstatus'],
									'cancelrejectreason': raw_response_dict[orderid]['cancelrejectreason'],
									# 'rejectedquantity': raw_response_dict[orderid]['rejectedquantity']
									'OrderAverageTradedPrice' : raw_response_dict[orderid]['OrderAverageTradedPrice']
								}

								all_final_response[all_collec].insert_one(final_post)
							
							else:
								final_post = {
									'quantity': quantity,
									'algoname': algoname,
									'instrumentID': symbol,
									'orderside' : orderside,
									'timestamp': timestamp,
									'orderstatus': orderstatus,
									'cancelrejectreason': cancelrejectreason,
									'rejectedquantity': rejectedquantity
								}
								nsecm_final_response[nsecm_collec].insert_one(final_post)
							# nsecm_final_response.'final_response_'+str(date).insert_one(final_post)
							del raw_response_dict[orderid]
							orderid_list.append(orderid)
							print(final_post)
			if orderid_list:
				for ord in orderid_list:
					del raw_dict[ord]

