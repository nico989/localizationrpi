from req import Req
import requests
import json
from requests.auth import HTTPBasicAuth

def main():
    #r=Req()
    #r = requests.get('http://pi:caramella98@192.168.1.69:2501/devices/views/all_views.json')
    #print(json.loads(r.content))
    url = 'http://pi:caramella98@192.168.1.69:2501/devices/views/phydot11_accesspoints/devices.json'
    head = {"Content-Type": "application/x-www-form-urlencoded; charset=utf-8"}
    j = { "devices" : "AC: 75: 1D: 57: 8A: D8" }
    dat = "json=" + json.dumps(j)
    print(dat)
    x = requests.post(url, headers=head)#, data=dat)
    print(x.status_code)
    print('\n')
    print(x.text)

main()
