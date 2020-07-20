# import json
import socket

class OrderSystem:

	# orderSock = socket.socket()
	# host = '192.168.0.102'  # Server IP
	# port = 40000
	#
	# try:
	# 	orderSock.connect((host, port))
	# 	print("Client Connected In Order System")
	#
	# except Exception as e:
	# 	print ('Error connecting Order Server', e)

	def directSend(self,orderDetails):
		message={}
		message['orderDetails'] = orderDetails
		message['algoName'] = 'Straddle Write 4x'
		print(message)
		# message=json.dumps(message)
		# self.orderSock.send(str.encode(message))
		# orderUniqueID=self.orderSock.recv(1024)
		# orderUniqueID=json.loads(message)
		orderUniqueID = 1000
		return orderUniqueID

	def place_order(self,exchangeSegment,exchangeInstrumentID,
				   productType,orderType,orderSide,orderQuantity):

		orderDetails={'algoName':'RMS','orderDetails':{'exchangeSegment': exchangeSegment, 'exchangeInstrumentID': exchangeInstrumentID,
							'productType': productType, 'orderType': orderType, 'orderSide': orderSide,
							'timeInForce': 'DAY', 'disclosedQuantity': 0,
							'orderQuantity': orderQuantity, 'limitPrice': 0, 'stopPrice': 0
							}}

		print(orderDetails)
		# orderDetails=json.dumps(orderDetails)
		# self.orderSock.send(str.encode(orderDetails))
		# orderUniqueID=self.orderSock.recv(1024)
		# orderUniqueID=json.loads(orderUniqueID)
		orderUniqueID=1000
		return orderUniqueID

# if __name__ == '__main__':
#   obj = OrderSystem()
#   obj.place_order('NSEFO', 47742,'MIS','MARKET','SELL',20)
