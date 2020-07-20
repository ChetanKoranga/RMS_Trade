import json
import ast
import pymongo
from pymongo import MongoClient
import datetime 
import time
import csv
import symphonyIdFetcher as sif
import OrderManagementSystem
import pandas as pd

omObj = OrderManagementSystem.OrderSystem()
date = datetime.date.today()
connection=MongoClient()
db=connection['Cumulative_symphonyorder']
collecName = f'cumulative_{date}'
cumulativeCollec = db[collecName]
clientList = []

with open(r'C:\Users\Mudraksh_Server1\Desktop\sparedux\squareoffUI\clientlist.txt', 'r') as f:
	for line in f:
		if line!='All\n' and line!='\n':
			clientList.append(line[:-1])
print(clientList)
targetUnit = 100
targetPutCount = {}
for client in clientList:
	targetPutCount[client] = 100
print(targetPutCount)
orderQuantity = 200
while True:
	currentPutCount = {}
	netPositionDf = pd.DataFrame(list(cumulativeCollec.find()))
	netPositionDf = netPositionDf[(netPositionDf['quantity']<0) & (netPositionDf['algoName'] == 'Reference')]
	if not netPositionDf.empty:
		for index, row in netPositionDf.iterrows():
			# print(row['quantity'])
			if row['symbol'][-2:] == 'PE':
				if row['clientID'] not in currentPutCount.keys():
					currentPutCount[row['clientID']] = abs(row['quantity'])
				else:
					currentPutCount[row['clientID']] += abs(row['quantity'])
		print(currentPutCount)
	else:
		print('No put found for this algo')

	if currentPutCount:
		for client in targetPutCount.keys():
			if client in currentPutCount.keys():
				if currentPutCount[client]>=targetPutCount[client]:
					print(f'Placing order for {orderQuantity} quantity in client {client}')
					targetPutCount[client]+=100

	time.sleep(5)

