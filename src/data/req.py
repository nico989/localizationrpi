import json, requests

class Req:
    def __init__(self):
        self._ipAddr = 'localhost'
        self._head = {"Content-Type": "application/x-www-form-urlencoded; charset=utf-8"}
        self._users = 'http://pi:caramella98@'
        self._port = 2501

    def setIP(self, ip):
        self._ipAddr = ip
    
    def getIP(self):
        return self._ipAddr

    def get(self, path, params):
        _url = self._users + self._ipAddr + ':' + str(self._port) + path
        response = requests.get(url=_url, params=params)
        if response.ok:
            return json.loads(response.text)

    def post(self, path, data):
        _url = self._users + self._ipAddr + ':' + str(self._port) + path
        dat = 'json=' + json.dumps(data)
        response = requests.post(url=_url, headers=self._head, data=dat)
        if response.ok:
            return json.loads(response.text)
