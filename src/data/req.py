import json, requests

class Req:
    def __init__(self, ipAddr=None):
        self._ipAddr = ipAddr or 'localhost'
        self._head = {"Content-Type": "application/x-www-form-urlencoded; charset=utf-8"}
        self._url = 'http://pi:caramella98@' + self._ipAddr +':2501'

    def get(self, path, params):
        response = requests.get(url=self._url+path, params=params)
        return json.loads(response.text)

    def post(self, path, data):
        dat = 'json=' + json.dumps(data)
        response = requests.post(url=self._url+path, headers=self._head, data=dat)
        return json.loads(response.text)
