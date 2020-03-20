import json, requests
from exception import HTTPError

class Req:
    def __init__(self, ipAddr=None):
        self._ipAddr = ipAddr or 'localhost'
        self._head = {"Content-Type": "application/x-www-form-urlencoded; charset=utf-8"}
        self._url = 'http://pi:caramella98@' + self._ipAddr +':2501'

    def get(self, path, params):
        response = requests.get(url=self._url+path, params=params)
        if(response.ok):
            return json.loads(response.text)
        else:
            raise HTTPError('HTTP request error')
        

    def post(self, path, data):
        dat = 'json=' + json.dumps(data)
        response = requests.post(url=self._url+path, headers=self._head, data=dat)
        if(response.ok):
            return json.loads(response.text)
        else:
            raise HTTPError('HTTP request error')
