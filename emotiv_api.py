import websocket
import ssl
import json

ws = websocket.create_connection('wss://emotivcortex.com:54321', sslopt={'cert_reqs': ssl.CERT_NONE})

class User:
    def __init__(self):
        self.username = ""
        self._auth = ""

emotiv_user = User()

def printResult(res):
    print(res)
    return res

def getLoggedUsers():
    ws.send(json.dumps({
        "jsonrpc": "2.0",
        "method": "getUserLogin",
        "id": 1
    }))
    return printResult(ws.recv())

def logout(username):
    ws.send(json.dumps({
        "jsonrpc": "2.0",
        "method": "logout",
        "params": {
            "username": username,
        },
        "id": 1
    }))
    return printResult(ws.recv())

def login(user):
    emotiv_user.username = user['username']
    ws.send(json.dumps({
        "jsonrpc": "2.0",
        "method": "login",
        "params": {
            "username": user['username'],
            "password": user['password'],
            "client_id": user['client_id'],
            "client_secret": user['client_secret']
        },
        "id": 1
    }))
    return printResult(ws.recv())

def authorize(user):
    global emotiv_user
    ws.send(json.dumps({
        "jsonrpc": "2.0",
        "method": "authorize",
        "params": {
            "client_id": user['client_id'],
            "client_secret": user['client_secret']
        },
        "id": 1
    }))
    res = ws.recv()
    result = json.loads(res)
    emotiv_user._auth = result['result']['_auth']
    return printResult(res)

def create_session():
    global emotiv_user
    ws.send(json.dumps({
        "jsonrpc": "2.0",
        "method": "createSession",
        "params": {
            "_auth": emotiv_user._auth,
            "headset": "EPOCPLUS-3B9AD65A",
            "status": "active"
        },
        "id": 1
    }))
    return printResult(ws.recv())

def accept_license():
    global emotiv_user
    ws.send(json.dumps({
        "jsonrpc": "2.0",
        "method": "acceptLicense",
        "params": {
            "_auth": emotiv_user._auth
        },
        "id": 1
    }))
    return printResult(ws.recv())

def query_sessions():
    global emotiv_user
    ws.send(json.dumps({
        "jsonrpc": "2.0",
        "method": "querySessions",
        "params": {
            "_auth": emotiv_user._auth
        },
        "id": 1
    }))
    return printResult(ws.recv())

def subscribe(type):
    global emotiv_user
    ws.send(json.dumps({
        "jsonrpc": "2.0",
        "method": "subscribe",
        "params": {
            "_auth": emotiv_user._auth,
            "streams": [
                type
            ]
        },
        "id": 1
    }))
    return printResult(ws.recv())

def unsubscribe(type):
    global emotiv_user
    ws.send(json.dumps({
        "jsonrpc": "2.0",
        "method": "unsubscribe",
        "params": {
            "_auth": emotiv_user._auth,
            "streams": [
                type
            ]
        },
        "id": 1
    }))
    return printResult(ws.recv())
