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

connection = MongoClient('localhost', 27017)
db = connection.exitpnl

__author__ = 'chetan'

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
app.config['DEBUG'] = True
# socketio = SocketIO(app, cors_allowed_origins="*")
socketio = SocketIO(app, cors_allowed_origins="*", async_mode=None, logger=False, engineio_logger=False)



def totalpnldata():
    # handle posts colection
    date = datetime.date.today()
    collec = f'exitpnl_{date}'

    while True:
        emitted = []
        # timestamp = str(datetime.datetime.now().time())
        data = db[collec]
        rec_data = data.find({}, {"_id": 0})
        for i in rec_data:
            # print(i)
            emitted.append(i)

        dictData = {'data': emitted}
        emt = json.dumps(dictData)
        # print(emt)
        socketio.emit('total_pnl', emt, broadcast=True)
        socketio.sleep(1)


@socketio.on('connect')
def socketcon():
    # need visibility of the global thread object
    print('Client connected')
    socketio.start_background_task(totalpnldata)


if __name__ == ("__main__"):
    socketio.run(app, host="192.168.0.103", port=5004)