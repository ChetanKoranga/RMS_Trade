import json
import socket
from math import floor
import sys, time
class OrderSystem:

	# clientMap = {'D7730003':1}#, 'D18138':0.1, 'D7730001':1}
	# lotSize = 20

	def directSend(self,orderDetails):
		message={}
		message['orderDetails'] = orderDetails
		message['algoName'] = 'Straddle Write 4x'
		print(message)
		message=json.dumps(message)
		self.orderSock.send(str.encode(message))
		orderUniqueID=self.orderSock.recv(1024)
		orderUniqueID=json.loads(message)
		orderUniqueID = 1000
		return orderUniqueID

	def place_order(self,exchangeSegment,exchangeInstrumentID,
				   productType,orderType,orderSide,orderQuantity, algoName, clientID, orderSock):

		orderDetails={'algoName':algoName,'orderDetails':{'exchangeSegment': exchangeSegment, 'exchangeInstrumentID': exchangeInstrumentID,
							'productType': productType, 'orderType': orderType, 'orderSide': orderSide,
							'timeInForce': 'DAY', 'disclosedQuantity': 0,
							'orderQuantity': orderQuantity, 'limitPrice': 0, 'stopPrice': 0, 'clientID':clientID
							}}

		print(orderDetails)
		orderDetails=json.dumps(orderDetails)
		orderSock.send(str.encode(orderDetails))
		orderUniqueID=orderSock.recv(1024)

	def placeSliceOrder(self,exchangeSegment,exchangeInstrumentID,
				   productType,orderType,orderSide,orderQuantity,algoName,clientID,
				   sliceSize, waitTime,authenticationKey):

		orderSock = socket.socket()
		host = '192.168.0.103'  # Server IP
		port = 40004

		try:
			orderSock.connect((host, port))
			print("Client Connected In Order System")
			key = json.dumps({'algoName':algoName,
								'authenticationKey':authenticationKey})
			orderSock.send(str.encode(key))
			verificationCheck=orderSock.recv(1024)
			print('Check: ', verificationCheck)
			verificationCheck = verificationCheck.decode("utf-8") 
			if verificationCheck != '1':
				raise Exception(verificationCheck)
				sys.exit(0)

		except Exception as e:
			raise Exception ('Error connecting Order Server', e)
			sys.exit(0)

		placeQuantity = orderQuantity

		while placeQuantity!=0:
			if placeQuantity>=sliceSize:
				self.place_order(exchangeSegment,exchangeInstrumentID,
								productType,orderType,orderSide,sliceSize,algoName, clientID, orderSock)
				placeQuantity-=sliceSize
			else:
				self.place_order(exchangeSegment, exchangeInstrumentID,
								 productType, orderType, orderSide, placeQuantity,algoName,clientID, orderSock)
				placeQuantity = 0
			time.sleep(waitTime)

		print('All quantity placed in client: ', clientID)
		orderSock.close()
		sys.exit(0)

	def quantityCal(self, quantity):
		lots = floor(quantity / self.lotSize)

		if lots == 0:
			return self.lotSize
		else:
			return lots * self.lotSize

if __name__ == '__main__':
	import secrets, sys

	authenticationKey = secrets.token_hex(2)
	print('Input the following authentication key in the server: ', authenticationKey)
	check = input('Ready to start algo? (y/n)')
	if check.upper() == 'Y':
		# authenticationKey = 'a12b'

		obj = OrderSystem()
		obj.placeSliceOrder('NSEFO', 48210,'MIS','MARKET','BUY',600,400,0.1, authenticationKey)
	# else:
	# 	sys.exit(0)