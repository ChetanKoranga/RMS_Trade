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

connection = MongoClient()
db = connection.clientWiseTotalPnl

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
app.config['DEBUG'] = True
# socketio = SocketIO(app, cors_allowed_origins="*")
socketio = SocketIO(app , cors_allowed_origins="*" , async_mode = None , logger = False , engineio_logger = False)


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)


def unRealizedData():
    # handle posts colection
    date = datetime.date.today()
    collec = f'clientWiseTotalPnl_{date}'

    while True:
        emitted = []
        # timestamp = str(datetime.datetime.now().time())
        data = db[collec]
        rec_data = data.find()
        for i in rec_data:
            # print(i)
            emitted.append(i)


        emt = JSONEncoder().encode(emitted)
        # print(emt)
        socketio.emit('unRealized_data', emt, broadcast=True)
        socketio.sleep(1)


@socketio.on('connect')
def socketcon():
    print('Client connected')
    print(request.sid)
    socketio.start_background_task(unRealizedData)


if __name__ == ("__main__"):
    socketio.run(app, host="192.168.0.103", port=5008)