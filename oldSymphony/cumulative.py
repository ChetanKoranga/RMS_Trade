# from facadeorder import XTconnect
# from Ordsocket_client import *
import threading
import socketserver
from datetime import datetime
import time
from random import randint
import json
# import pymongo
# from pymongo import MongoClient
import pymongo
from pymongo import MongoClient
import datetime

client=MongoClient()

db=client['symphonyorder']



print("check statment")

def connectSocket(token):
	sk=socket_io(token)
	socketconnect=sk.connect()

'''login to broker api'''
# xt = XTconnect()
# """redirect the user to the login url obtained
# from xt.login_url(), and receive the token"""
# xt.login('MUDRAKSH', 'Mu@12345', 'e1e3ed9957977332', 'WEBAPI')
# set_token = xt.set_token
# with open('token.txt', 'w') as f:
# 	f.write(set_token)
# 	f.close()
# """connected to the socket"""
# threading.Thread(target=connectSocket, args=(set_token,)).start()


'''------------------order server code starts below-------------'''

class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):

	def handle(self):
		cur_thread = threading.current_thread()
		try:
			date = datetime.date.today()
			while True:
				orderDetails = self.request.recv(2048)
				# print(orderDetails)
				orderDetails = json.loads(orderDetails)
				# print("received: ", orderDetails, 'in:', cur_thread, 'at', datetime.now().time())
				order=orderDetails['orderDetails']
				print(orderDetails)
				orderUniqueIdentifier=str(randint(10000,1000000))
				order['orderUniqueIdentifier']=orderUniqueIdentifier
				# xt.placeOrder(orderDetails)
				self.request.send(str.encode(orderUniqueIdentifier))
				# algoName=orderDetails['orderDetails']['orderType']
				# print(algoName)

				data1=orderDetails['algoName']
				data2=orderDetails['orderDetails']['orderQuantity']
				data3=orderDetails['orderDetails']['exchangeSegment']
				data4=orderDetails['orderDetails']['orderSide']
                # print(data1)
                # print(data2)
                # print(data3)
                # print(data4)
                post={
				"algoName":data1,
				"symbol":data3,
				"quantity":data2,
				"buy_sell":data4,
				"time_stamp": str(datetime.datetime.now().time())
				}
                collec = f'orders_{date}'
                
                try:
                    db.create_collection(collec)
	    			# posts = db.collec
    				db[collec].insert(post)
                except Exception:
                    match = db[collec].find( { $and: [{"algoName":data1}, {"symbol": data3}] })
                    print(match)
				

		except Exception as e:
			print(e)


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
	pass

if __name__ == '__main__':

	''' host and port when the gdf server would run'''
	host, port = "192.168.1.6", 42612
	# host, port = "192.168.0.113", 42612

	server = ThreadedTCPServer((host, port), ThreadedTCPRequestHandler)
	ip, port = server.server_address

	''' start a thread with the server -- that thread will then start one
		 more thread for each request'''
	server_thread = threading.Thread(target=server.serve_forever)
	server_thread.daemon = False
	server_thread.start()
	print("server loop running in thread:", server_thread.name)