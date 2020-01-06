from flask import Flask
from flask_socketio import SocketIO, send, emit
from bson import ObjectId
import os
import json
import socket
from pathlib import Path
from time import sleep
import pymongo
from pymongo import MongoClient
# import pprint
import datetime


connection = MongoClient('localhost', 27017)
db = connection.Cumulative_symphonyorder

__author__ = 'chetan'

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
app.config['DEBUG'] = True
# socketio = SocketIO(app, cors_allowed_origins="*")
socketio = SocketIO(app, cors_allowed_origins="*", async_mode=None, logger=False, engineio_logger=False)

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)

def cumulativedata():
    # handle posts colection
    date = datetime.date.today()
    collec = f'cumulative_{date}'

    while True:
        emitted = []
        # timestamp = str(datetime.datetime.now().time())
        data = db[collec]
        rec_data = data.find()
        for i in rec_data:
            # print(i)
            emitted.append(i)

        dictData = {'data': emitted}
        emt = JSONEncoder().encode(dictData)
        # print(emt)
        socketio.emit('cumulative_data', emt, broadcast=True)
        socketio.sleep(1)


@socketio.on('connect')
def socketcon():
    # need visibility of the global thread object
    print('Client connected')
    socketio.start_background_task(cumulativedata)


if __name__ == ("__main__"):
    # socketio.run(app, host="192.168.1.6", port=5002)
    socketio.run(app, host="192.168.43.188", port=5002)