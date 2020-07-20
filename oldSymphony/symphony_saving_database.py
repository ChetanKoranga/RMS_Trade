# from facadeorder import XTconnect
# from Ordsocket_client import *
import threading
import socketserver
# from datetime import datetime
import time
from random import randint
import json
from demoMongo import savedata
# import pymongo
# from pymongo import MongoClient
import pymongo
from pymongo import MongoClient
import datetime

date = datetime.date.today()
collec = f'orders_{date}'
try:
	mongocl = MongoClient()
	db = mongocl['symphonyorder_raw']
	db.create_collection(collec)
	print("Collection created successfully.")
except Exception:
	if db['symphonyorder_raw']:
		pass
	else:
		print("ERROR: Mongo Connection Error")

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
			while True:
				orderDetails = self.request.recv(2048)

				orderDetails = json.loads(orderDetails)
				order = orderDetails['orderDetails']
				orderUniqueIdentifier = str(randint(10000, 1000000))
				order['orderUniqueIdentifier'] = orderUniqueIdentifier
				print('To place:', order)
				# xt.placeOrder(order)
				self.request.send(str.encode(orderUniqueIdentifier))
				order['algoName'] = orderDetails['algoName']
				print (order)
				db[collec].insert_one(order)
				print("Received and logged: ", order, 'in:', cur_thread, 'at', datetime.datetime.now().time())

		except Exception as e:
			print(e)

class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
	pass

if __name__ == '__main__':

	''' host and port when the gdf server would run'''
	host, port = "192.168.0.103", 42612
	# host, port = "192.168.0.113", 42612

	server = ThreadedTCPServer((host, port), ThreadedTCPRequestHandler)
	ip, port = server.server_address

	''' start a thread with the server -- that thread will then start one
		 more thread for each request'''
	server_thread = threading.Thread(target=server.serve_forever)
	server_thread.daemon = False
	server_thread.start()
	print("server loop running in thread:", server_thread.name)
