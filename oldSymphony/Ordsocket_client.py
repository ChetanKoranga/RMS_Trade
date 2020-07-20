import json
import socketio
import threading
import time
import pymongo
from pymongo import MongoClient
import datetime
import json
import ast
import queue
# from datetime import date
# from collection import dequeue
l=queue.Queue(maxsize=100)

date = datetime.date.today()
client=MongoClient()

# name_db='order_log_raw_' + str(datetime.date.today())

db=client['response_data']
collec = f'orderResponses_{date}'
# collection=db['orderlog']
try:
    db.create_collection(collec)
except:
    pass

file='tradeLog.txt'

def responseLogger():
    while True:
        if not l.empty():
            upload = ast.literal_eval(json.loads(l.get()))
            db[collec].insert_one(upload)
        time.sleep(0.1)

t1 = threading.Thread(target = responseLogger)
t1.start()

class socket_io(socketio.Client):
    """A Socket.IO client.
    This class implements a fully compliant Socket.IO web client with support
    for websocket and long-polling transports.
    :param reconnection: 'True'. if the client should automatically attempt to
                         reconnect to the server after an interruption, or
                         'False' to not reconnect. The default is 'True'.
    :param reconnection_attempts: How many reconnection attempts to issue
                                  before giving up, or 0 for infinity attempts.
                                  The default is 0.
    :param reconnection_delay: How long to wait in seconds before the first
                               reconnection attempt. Each successive attempt
                               doubles this delay.
    :param reconnection_delay_max: The maximum delay between reconnection
                                   attempts.
    :param randomization_factor: Randomization amount for each delay between
                                 reconnection attempts. The default is 0.5,
                                 which means that each delay is randomly
                                 adjusted by +/- 50%.
    :param logger: To enable logging set to 'True' or pass a logger object to
                   use. To disable logging set to 'False'. The default is
                   'False'.
    :param binary: 'True' to support binary payloads, 'False' to treat all
                   payloads as text. On Python 2, if this is set to 'True',
                   'unicode' values are treated as text, and 'str' and
                   'bytes' values are treated as binary.  This option has no
                   effect on Python 3, where text and binary payloads are
                   always automatically discovered.
    :param json: An alternative json module to use for encoding and decoding
                 packets. Custom json modules must have 'dumps' and 'loads'
                 functions that are compatible with the standard library
                 versions.
    """
    def __init__(self,token,reconnection=True, reconnection_attempts=0, reconnection_delay=1, reconnection_delay_max=5, randomization_factor=0.5, logger=False, binary=False, json=None, **kwargs):
        self.sid =socketio.Client()
        self.sid.on('connect', self.on_connect)
        self.sid.on('message', self.on_message)
        self.sid.on('joined', self.on_joined)
        self.sid.on('error', self.on_error)
        self.sid.on('order',self.on_order)
        self.sid.on('trade',self.on_trade)
        self.sid.on('position',self.on_position)
        self.sid.on('logout',self.on_messagelogout)
        # self.sid.on('Thread',self.start_thrading)
        self.sid.on('disconnect', self.on_disconnect)

        userID='D7730001'
        # self.token= "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySUQiOiJBSklUS1VNQVIxIiwicHVibGljS2V5IjoiZTRkMzI1ZjI2Y2U1MjI3OCIsImlhdCI6MTU2MjMxNTg2MSwiZXhwIjoxNTYyNDAyMjYxfQ.0lFZInAdNKQzT8v7cDqVbvaD-qW6bbE52wRecpY-4Ho"
        token=token
        port='http://xts.nirmalbang.com:3002/?token='
        self.connection_url =port+token+'&userID='+userID

    def connect(self,headers={}, transports='websocket', namespaces=None, socketio_path='/interactive/socket.io'):
        """Connect to a Socket.IO server.
        :param url: The URL of the Socket.IO server. It can include custom
                    query string parameters if required by the server.
        :param headers: A dictionary with custom headers to send with the
                        connection request.
        :param transports: The list of allowed transports. Valid transports
                           are 'polling' and 'websocket'. If not
                           given, the polling transport is connected first,
                           then an upgrade to websocket is attempted.
        :param namespaces: The list of custom namespaces to connect, in
                           addition to the default namespace. If not given,
                           the namespace list is obtained from the registered
                           event handlers.
        :param socketio_path: The endpoint where the Socket.IO server is
                              installed. The default value is appropriate for
                              most cases.

        """
        """Connect to the socket."""
        url = self.connection_url
        self.sid.connect(url,headers,transports,namespaces,socketio_path)
        self.sid.wait()
        """Disconnect from the socket."""
        self.sid.disconnect()
    
    def on_connect(self):
        """Connect from the socket."""
        print('Interactive socket connected successfully!')

    def on_message(self):
        print('I received a message!')

    def on_joined(self,data):
        print('Interactive socket joined successfully!'+data)

    def on_error(self,data):
        print('Interactive socket error!'+data)


    ''''Order status is recv. below'''
    def on_order(self,data):
        # check=dequeue()
        l.put(data)
        # # time.sleep(2)
        # new=l.get()
        # upload=json.loads(new)
        # print("Order placed!"+data)
        # pass
    def on_trade(self,data):
         pass
    ''''_____________________'''

    def on_position(self,data):
        # print("Position Retrived!"+data)
        pass

    def on_messagelogout(self):
        print("User logged out!")
  
    def on_disconnect(self): 
        print('Socket disconnected!')

# if __name__ == '__main__':
#     socket_io().connect()
