from facadeorder import XTconnect
# from Ordsocket_client import *
import threading
import socketserver
from datetime import datetime
import time
from random import randint
import json
import pymongo
import pymongo
from pymongo import MongoClient
import csv
import pymongo
import datetime as dt

date = dt.date.today()
client = MongoClient()

db = client['symphonyorder']

collection = db[f'orderDetails']

print("check statment")

'''Below order is to generate a mapping of Symbol ids and name for XTS API'''

class CsvToDict:

    optionIDSymname={}
    reader = csv.reader(open(r'OptionIds.txt', 'r'))
    for row in reader:
        v1,k=row
        optionIDSymname[v1]=k

    futIDSymname = {}
    reader = csv.reader(open(r'FuturesIds.txt', 'r'))
    for row in reader:
        v1, k = row
        futIDSymname[v1] = k
    commodityIDSymname = {}
    # reader = csv.reader(open(r'MCXIds.txt', 'r'))
    for row in reader:
        v1, k = row
        # commodityIDSymname[v1] = k
    stocksIDSymname = {}
    reader = csv.reader(open(r'stocksIds.txt', 'r'))
    for row in reader:
        v1, k = row
        stocksIDSymname[v1] = k
    # print(optionIDSymname)

def connectSocket(token):
    sk = socket_io(token)
    socketconnect = sk.connect()

# idMapObj=CsvToDict()

'''login to broker api'''
xt = XTconnect()
"""redirect the user to the login url obtained
from xt.login_url(), and receive the token"""
xt.login('MUDRAKSH', 'Mu@12345', 'e1e3ed9957977332', 'WEBAPI')
# set_token = xt.set_token
# with open('token.txt', 'w') as f:
	# f.write(set_token)
	# f.close()
"""connected to the socket"""
# threading.Thread(target=connectSocket, args=(set_token,)).start()

'''------------------order server code starts below-------------'''

class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):

    def handle(self):
        cur_thread = threading.current_thread()
        try:
            while True:
                orderDetails = self.request.recv(2048)
                # print(orderDetails)
                orderDetails = json.loads(orderDetails)
                print("received: ", orderDetails, 'in:', cur_thread, 'at', datetime.now().time())
                order = orderDetails['orderDetails']

                orderUniqueIdentifier = str(randint(10000, 1000000))
                order['orderUniqueIdentifier'] = orderUniqueIdentifier
                xt.placeOrder(order)
                self.request.send(str.encode(orderUniqueIdentifier))
                # algoName=orderDetails['orderDetails']['orderType']
                # print(algoName)
                # print("check statment for details ")
                data1 = orderDetails['algoName']
                data2 = orderDetails['orderDetails']['orderQuantity']
                data3 = orderDetails['orderDetails']['exchangeSegment']
                data4 = orderDetails['orderDetails']['orderSide']
                if data3=='NSEFO':
                    if orderDetails['orderDetails']['exchangeInstrumentID'] in idMapObj.optionIDSymname.keys():
                        data5=idMapObj.optionIDSymname[orderDetails['orderDetails']['exchangeInstrumentID']]
                    else:
                        data5 = idMapObj.futIDSymname[orderDetails['orderDetails']['exchangeInstrumentID']]
                if data3 == 'MCXFO':
                     data5 = idMapObj.commodityIDSymname[orderDetails['orderDetails']['exchangeInstrumentID']]
                if data3=='NSECM':
                    data5 = idMapObj.stocksIDSymname[orderDetails['orderDetails']['exchangeInstrumentID']]

                # print(data1)
                # print(data2)
                # print(data3)
                # print(data4)

                post=[{
				"algoName":data1,
				"symbol":data5,
				"quantity":data2,
				"buy_sell":data4,
				"time_stamp": str(datetime.datetime.now().time())
				}]

                posts = db.posts
                posts.insert(post)

        except Exception as e:
            print(e)


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass


if __name__ == '__main__':
    ''' host and port when the gdf server would run'''
    host, port = "192.168.1.80", 42612

    server = ThreadedTCPServer((host, port), ThreadedTCPRequestHandler)
    ip, port = server.server_address

    ''' start a thread with the server -- that thread will then start one
         more thread for each request'''
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = False
    server_thread.start()
    print ("server loop running in thread:", server_thread.name)

