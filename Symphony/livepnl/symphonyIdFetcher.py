import socket, json

def connect(symDict):
    sock = socket.socket()
    port = 40123
    sock.connect(('192.168.0.103', port))
    sendData = json.dumps(symDict)
    sock.send(str.encode(sendData))
    symIds= sock.recv(2048)
    symIds= json.loads(symIds)
    sock.close()
    return symIds

