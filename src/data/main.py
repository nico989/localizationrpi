#from req import Req
import requests
import json
from requests.auth import HTTPBasicAuth

def main():
    #r=Req()
    #r = requests.get('http://pi:caramella98@192.168.1.69:2501/devices/views/all_views.json')
    #print(json.loads(r.content))
    url = 'http://192.168.1.69:2501/devices/views/all/devices.json'
    x = requests.post(url, auth=HTTPBasicAuth('pi', 'caramella98'))
    print(x.status_code)

main()
