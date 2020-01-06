from flask import Flask
from flask_socketio import SocketIO, send, emit
import os
import json
import socket
from pathlib import Path
from time import sleep
import pymongo
from pymongo import MongoClient
# import pprint
import datetime

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

connection = MongoClient('localhost', 27017)
# print("Yey")
db = connection.Cumulative_symphonyorder

@socketio.on('loop_event')
@socketio.on('connect')
def algodata():
	# handle posts colection
	date = datetime.date.today()
	collec = f'cumulative_{date}'
	emitted = []
	# timestamp = str(datetime.datetime.now().time())
	data = db[collec]
	rec_data = data.find({}, { "_id": 0 })
	for i in rec_data:
		# print(i)
		emitted.append(i)

	dictData = {'data': emitted}
	# print
	emt = json.dumps(dictData)
	# print(emt)
	socketio.send(emt, broadcast=True)
	
		
	# data = client.posts.find()
	# print(data)
	#  restaurants.find().limit(10):
		#  pprint.pprint(record)
	
	# print('yoooo')
	# restaurants = db.restaurants
	# print('Total Record for the collection: ' + str(restaurants.count()))
	# for record in restaurants.find().limit(10):
	#      pprint.pprint(record)


if __name__ == ("__main__"):

	socketio.run(app,host="192.168.0.102", port=5002)
