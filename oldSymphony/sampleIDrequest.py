import socket, json
import sampleOrder
import time
# import OrderManagementSystem.OrderManagementSystem as po


def connect(symDict):
    sock = socket.socket()
    port = 40123
    # sock.connect(('192.168.0.113', port))
    sock.connect(('192.168.1.80', port))
    sendData = json.dumps(symDict)
    sock.send(str.encode(sendData))
    symIds= sock.recv(2048)
    symIds= json.loads(symIds)
    sock.close()
    return symIds

IDS=connect(symDict={'BANKNIFTY03OCT1930200CE':{'exchangeSegment':'OPTIDX'},
                 'BANKNIFTY03OCT1930100PE':{'exchangeSegment':'OPTIDX'}})
                 # 'BANKBANKNIFTY26SEP1928200CE':{'exchangeSegment':'OPTIDX'}})
orderNums=[]
print(IDS)

orderObj=sampleOrder.orderMaker()
orderNums.append(orderObj.placeOrder('52285',IDS['BANKNIFTY03OCT1930200CE'],'NRML','MARKET','BUY',550,'11111'))
# orderNums.append(orderObj.placeOrder('52285',IDS['BANKNIFTY03OCT1930100PE'],'NRML','MARKET','BUY',550,'DemoAlgo63'))
# orderNums.append(orderObj.placeOrder('52285',IDS['BANKNIFTY03OCT1930200CE'],'NRML','MARKET','BUY',550,'DemoAlgo68783'))
# orderNums.append(orderObj.placeOrder('52285',IDS['BANKNIFTY03OCT1930200CE'],'NRML','MARKET','BUY',550,'DemoAlgo63'))
# orderNums.append(orderObj.placeOrder('52285',IDS['BANKNIFTY03OCT1930200CE'],'NRML','MARKET','BUY',550,'DemoAlgo63657'))
# orderNums.append(orderObj.placeOrder('52285',IDS['BANKNIFTY03OCT1930200CE'],'NRML','MARKET','BUY',550,'DemoAlgo63345'))
# orderNums.append(orderObj.placeOrder('52285',IDS['BANKNIFTY03OCT1930200CE'],'NRML','MARKET','SELL',550,'DddddemoAlgo63'))
