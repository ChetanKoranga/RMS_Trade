from flask import Flask,request
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
from bson import ObjectId

connection = MongoClient('localhost', 27017)
response_db = connection.final_response

__author__ = 'mudraksh!'

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
app.config['DEBUG'] = True
# socketio = SocketIO(app, cors_allowed_origins="*")
socketio = SocketIO(app, cors_allowed_origins="*", async_mode=None, logger=False, engineio_logger=False)

# class JSONEncoder(json.JSONEncoder):
#     def default(self, o):
#         if isinstance(o, ObjectId):
#             return str(o)
#         return json.JSONEncoder.default(self, o)

def responsedata():
    # handle posts colection
    date = datetime.date.today()
    collec = f'final_response_{date}'

    while True:
        emitted = []
        # timestamp = str(datetime.datetime.now().time())
        data = response_db[collec]
        rec_data = data.find({},{"_id":0})
        for i in rec_data:
            # print(i['_id'])
            emitted.append(i)

        
        # print(dictData)

        # print(emt)
        socketio.emit('filter_response_data', emitted, broadcast=True)
        socketio.sleep(2)


@socketio.on('connect')
def socketcon():
    # need visibility of the global thread object
    print('Client connected')
    print(request.sid)
    socketio.start_background_task(responsedata)


if __name__ == ("__main__"):
    # socketio.run(app, host="192.168.1.6", port=5003)
    socketio.run(app, host="localhost", port=5013)
