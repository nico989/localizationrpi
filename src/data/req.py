import json, requests
from exception import HTTPError
class Req:
    def __init__(self, ipAddr):
        self.__ipAddr = ipAddr
        self.__head = {"Content-Type": "application/x-www-form-urlencoded; charset=utf-8"}
        self.__url = 'http://pi:caramella98@' + self.__ipAddr +':2501'

    def get(self, path, params):
        response = requests.get(url=self.__url+path, params=params)
        if(response.ok):
            return json.loads(response.text)
        else:
            raise HTTPError('HTTP request error')
        

    def post(self, path, data):
        dat = 'json=' + json.dumps(data)
        response = requests.post(url=self.__url+path, headers=self.__head, data=dat)
        if(response.ok):
            return json.loads(response.text)
        else:
            raise HTTPError('HTTP request error')
