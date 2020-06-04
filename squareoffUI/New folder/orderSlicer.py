import json
import socket
import time
import sys, os

class OrderSystem2:

	def directSend(self,orderDetails):
		message={}
		message['orderDetails'] = orderDetails
		message['algoName'] = 'Ravi News Partial Booking'
		print(message)
		message=json.dumps(message)
		self.orderSock.send(str.encode(message))
		orderUniqueID=self.orderSock.recv(1024)
		orderUniqueID=json.loads(message)
		# orderUniqueID = 1000
		return orderUniqueID

	def place_order(self,exchangeSegment,exchangeInstrumentID,
				   productType,orderType,orderSide,orderQuantity,
					algoName,clientID, sliceSize, lotSize, waitTime ):

		if sliceSize%lotSize == 0:
			self.orderSock = socket.socket()
			host = '192.168.0.103'  # Server IP
			port = 40004

			try:
				self.orderSock.connect((host, port))
				print("Client Connected In Order System")

			except Exception as e:
				raise Exception('Error connecting Order Server', e)
			sliceCount = 0
			print('sliceSize ', sliceSize)
			print('Order quan: ', orderQuantity)
			lastCount =0
			orderQuantity -=sliceSize
			while orderQuantity!=0:
				# orderQuantity = sliceSize
				orderDetails={'algoName':algoName,'orderDetails':{'exchangeSegment': exchangeSegment,
									'exchangeInstrumentID': exchangeInstrumentID,'productType': productType,
									'orderType': orderType, 'orderSide': orderSide,
									'timeInForce': 'DAY', 'disclosedQuantity': 0,
									'orderQuantity': sliceSize, 'limitPrice': 0,
									'stopPrice': 0,'clientID': clientID
									}}
				print(orderDetails)
				orderDetails=json.dumps(orderDetails)
				self.orderSock.send(str.encode(orderDetails))
				_ = self.orderSock.recv(256)
				print('Order quantity: ', orderQuantity)
				temp  = orderQuantity - sliceSize
				if temp == 0:
					print(f'Placed the entire order in {os.getpid()}')
					self.orderSock.close()
					sys.exit(0)
				if temp>0:
					orderQuantity -= sliceSize
				else:
					sliceSize = orderQuantity
				# if orderQuantity>sliceSize:
				# 	orderQuantity-=sliceSize
				#
				# else:
				# 	lastCount+=1
				# 	sliceSize =  orderQuantity
				# 	if lastCount == 2:
						# orderQuantity = 0
						# print(f'Placed the entire order in {os.getpid()}')
						# self.orderSock.close()
						# sys.exit(0)
				# if orderQuantity <0:
				# 	# sliceSize = orderQuantity + sliceSize
				# 	# orderQuantity = sliceSize
				# 	# print('Last order quantity: ', orderQuantity)
				# 	orderQuantity = abs(orderQuantity)
				# 	sliceSize = orderQuantity
				sliceCount+=1
				print(sliceCount)
				time.sleep(waitTime)
			

		else:
			raise Exception('Incorrect slice size provided!!')

# if __name__ == '__main__':
#   obj = OrderSystem2()
#   p1 = mp.Process(target=obj.place_order, args = ('NSEFO',12345,'MIS',
# 				  'MARKET','BUY',{'D7730001': 400, 'D18138':400},
# 				  100)).start()
  # p2 = mp.Process(target=obj.place_order, args=('NSEFO', 243234, 'MIS',
	# 											'MARKET', 'SELL', {'D7730001': 400, 'D18138': 400},
	# 											60)).start()
# print('Order sent to slicer...')
  # obj.place_order(exchangeSegment='NSEFO',exchangeInstrumentID=12345, productType='MIS',
	# 			  orderType='MARKET',orderSide='BUY',clientMap={'D7730001': 400, 'D18138':400},
	# 			  sliceSize=60)
