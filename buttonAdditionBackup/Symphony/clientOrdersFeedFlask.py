from flask import Flask, request
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
date = datetime.date.today()
clientOrder_collec = f"client_orders_{date}"
clientOrder_db = connection.client_order_log[clientOrder_collec]

__author__ = 'mudraksh!'

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
app.config['DEBUG'] = True
# socketio = SocketIO(app, cors_allowed_origins="*")
socketio = SocketIO(app, cors_allowed_origins="*",
                    async_mode=None, logger=False, engineio_logger=False)


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)


def clientOrdersFeed():

    while True:
        emitted = []
        # timestamp = str(datetime.datetime.now().time())
        data = clientOrder_db
        rec_data = data.find()
        for i in rec_data:
            # print(i['_id'])
            emitted.append(i)

        # print(dictData)
        emt = JSONEncoder().encode(emitted)
        # print(emt)
        socketio.emit('clientOrder_data', emt, broadcast=True)
        socketio.sleep(1)


@socketio.on('connect')
def socketcon():
    # need visibility of the global thread object
    print('Client connected')
    print(request.sid)
    socketio.start_background_task(clientOrdersFeed)


if __name__ == ("__main__"):
    # socketio.run(app, host="192.168.1.6", port=5003)
    socketio.run(app, host="192.168.0.103", port=5007)
