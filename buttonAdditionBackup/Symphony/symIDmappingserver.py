import csv
import threading
import socketserver
import json
from datetime import datetime

'''Below order is to generate a mapping of Symbol ids and name for XTS API'''

class CsvToDict:

    optionIDSymname={}
    reader = csv.reader(open(r'OptionIds.txt', 'r'))
    for row in reader:
        v1,k=row
        optionIDSymname[k]=v1

    futIDSymname = {}
    reader = csv.reader(open(r'FuturesIds.txt', 'r'))
    for row in reader:
        v1, k = row
        futIDSymname[k] = v1
obj = CsvToDict()
optionMap = obj.optionIDSymname
futureMap= obj.futIDSymname
'''Below code is to start the server that will send Symbol IDs for respective symbol names'''
class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):

    def handle(self):
        cur_thread = threading.current_thread()
        symDetails = self.request.recv(2048)
        symDetails = json.loads(symDetails)
        symIdDict={}
        print("Received: ", symDetails, 'in:', cur_thread, 'at', datetime.now().time())
        for key in symDetails:
            print(key,symDetails[key])
            if symDetails[key]['exchangeSegment'] == 'FUTSTK' or symDetails[key]['exchangeSegment'] == 'FUTIDX':
                try:symIdDict[key]=futureMap[key]
                except:symIdDict[key]='Not Found'

            elif symDetails[key]['exchangeSegment'] == 'OPTIDX':
                try:symIdDict[key] = optionMap[key]
                except:symIdDict[key]='Not Found'
        sendData=json.dumps(symIdDict)
        self.request.send(str.encode(sendData))

class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

if __name__=='__main__':
    ''' host and port when the gdf server would run'''
    host, port = "192.168.1.6", 40123
    # host, port = "192.168.0.113", 40123
    server = ThreadedTCPServer((host, port), ThreadedTCPRequestHandler)
    ip, port = server.server_address

    ''' start a thread with the server -- that thread will then start one
         more thread for each request'''
    server_thread = threading.Thread(target=server.serve_forever)
    # server_thread.daemon = True
    server_thread.start()
    print("server loop running in thread:", server_thread.name)
