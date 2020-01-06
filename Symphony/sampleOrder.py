import json
import socket
import time
class orderMaker:

	orderSock = socket.socket()
	host = '192.168.1.80'  # Server IP
	# host = '192.168.0.113'
	port = 42612
	
	try:
		orderSock.connect((host, port))
		print("Client Connected In Order System")
	
	except Exception as e:
		print ('Error connecting Order Server', e)
	#
	# feedbackSock = socket.socket()
	# feedbackHost = '192.168.1.80'  # Server IP
	# feedBackPort = 40012

	# try:
	# 	feedbackSock.connect((feedbackHost, feedBackPort))
	# 	print("Client Connected to Feedback server")
	#
	# except Exception as e:
	# 	print ('Error connecting Feedback Server', e)


	def placeOrder(self,exchangeSegment,exchangeInstrumentID,
				   productType,orderType,orderSide,orderQuantity, algoName):

		orderDetails={'orderDetails':{'exchangeSegment': exchangeSegment, 'exchangeInstrumentID': exchangeInstrumentID,
							'productType': productType, 'orderType': orderType, 'orderSide': orderSide,
							'timeInForce': 'DAY', 'disclosedQuantity': 0,
							'orderQuantity': orderQuantity, 'limitPrice': 0, 'stopPrice': 0
							},'algoName':algoName}
		# with open("log.json", "a") as write_file:
		# 	json.dump(orderDetails, write_file, indent=1)
		# json.dump(orderDetails, 'log.txt')
		orderDetails=json.dumps(orderDetails)
		self.orderSock.send(str.encode(orderDetails))
		orderUniqueID=self.orderSock.recv(1024)
		orderUniqueID=json.loads(orderUniqueID)
		return str(1000)

	# def getFeedback(self, orderID):
	# 	sendData=json.dumps(orderID)
	# 	self.feedbackSock.send(str.encode(orderID))
	# 	feedback=self.feedbackSock.recv(1024)
	# 	# print('feedback:', feedback)
	# 	feedback=json.loads(feedback)
	# 	self.feedbackSock.send(str.encode('AWK'))
	# 	return feedback

