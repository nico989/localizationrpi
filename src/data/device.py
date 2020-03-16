from req import Req
from exception import HTTPError

class Device:
    def __init__(self, ipAddr):
        self._req = Req(ipAddr)
        self._fields = {'fields': ['kismet.device.base.commonname',
                                    'kismet.device.base.channel',
                                    'kismet.device.base.signal/kismet.common.signal.last_signal',
                                    'kismet.device.base.name',
                                    'kismet.device.base.macaddr',
                                    'kismet.device.base.type',
                                    'kismet.device.base.first_time' # timpestamp della prima volta che ho visto il dispositivo
                                    'kismet.device.base.last_time' # timpestamp dell'ultima volta che ho visto il dispositivo
                                    'kismet.device.base.frequency'
                                    ]}
    
    def getAll(self):
        try:
            return self._req.post('/devices/views/phy-IEEE802.11/devices.json', self._fields)
        except HTTPError as error:
            return error

    def getAccessPoint(self):
        try:
            return self._req.post('/devices/views/phydot11_accesspoints/devices.json', self._fields)
        except HTTPError as error:
            return error

    def getClient(self):
        try:
            client = []
            dev = self._req.post('/devices/views/phy-IEEE802.11/devices.json', self._fields)
            for d in dev:
                if d['kismet.device.base.type'] == 'Wi-Fi Client':
                    client.append(d)
            return client
        except HTTPError as error:
            return error

    def find(self, devices, fields, filt):
        listDev = []
        for dev in devices:
            if(dev[fields] == filt):
                listDev.append(dev)
        return listDev
    
    def filter(self, devices, fields):
        listDev = []
        for dev in devices:
            for f in fields:
                listDev.append(dev[f])
        return listDev
