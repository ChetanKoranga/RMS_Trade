from flask import Flask
from flask_socketio import SocketIO, send, emit
import os
import json
import socket
from pathlib import Path
from time import sleep
import pymongo
from pymongo import MongoClient
from bson import ObjectId
# import pprint
import datetime

connection = MongoClient('localhost', 27017)
db = connection.symphonyorder_netquantity


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



def netclientdata():
    # handle posts colection
    date = datetime.date.today()
    collec = f'symphonyorder_netquantity_{date}'

    while True:
        emitted = []
        # timestamp = str(datetime.datetime.now().time())
        data = db[collec]
        rec_data = data.find({})
        for i in rec_data:
            # print(i)
            emitted.append(i)

        dictData = {'data': emitted}
        emt = JSONEncoder().encode(dictData)
        # print(emt)
        socketio.emit('netClient_data', emt, broadcast=True)
        socketio.sleep(1)


@socketio.on('connect')
def socketcon():
    # need visibility of the global thread object
    print('Client connected')
    socketio.start_background_task(netclientdata)


if __name__ == ("__main__"):
    socketio.run(app, host="192.168.0.103", port=5005)