from req import Req
from exception import IPError
from mathOperation import arithmeticMean, truncate

class Device:
    def __init__(self, ipAddr):
        self._req = Req(ipAddr)
        self._paths = ['/devices/views/phy-IEEE802.11/devices.json', '/devices/views/phydot11_accesspoints/devices.json', 
                       '/system/timestamp.json', '/devices/by-mac/', '/devices.json']
        self._fields = {'fields': [ 'kismet.device.base.macaddr',
                                    'kismet.device.base.manuf',
                                    'kismet.device.base.channel',
                                    'kismet.device.base.frequency',
                                    'kismet.device.base.signal/kismet.common.signal.last_signal',
                                    'kismet.device.base.type',
                                    'kismet.device.base.last_time'
                                    ]}
        self._K = 15.08085
        self._A = -43.7257

    def setIndoor(self):
        self._K = 15.08085
        self._A = -43.7257

    def setOutdoor(self):
        self._K = 0.0
        self._A = 0.0

    def getAll(self):
        try:
            return self._req.post(self._paths[0], self._fields)
        except:
            raise IPError('Wrong IP')
        
    def getAccessPoint(self):
        try:
            return self._req.post(self._paths[1], self._fields)
        except:
            raise IPError('Wrong IP')

    def getDeviceByMAC(self, macAddr):
        try:
            return self._req.post(self._paths[3] + macAddr + self._paths[4] , self._fields)
        except:
            raise IPError('Wrong IP')

    def getClients(self):
        try:
            clients = []
            devices = self._req.post(self._paths[0], self._fields)
            for device in devices:
                if device[self._fields['fields'][5]]=='Wi-Fi Client':
                    clients.append(device)
            return clients
        except:
            raise IPError('Wrong IP')

    def getClientsLastTimeSec(self, time):
        try:
            clients = []
            initialTime = self._req.get(self._paths[2], None)
            devices = self._req.post(self._paths[0], self._fields)
            for device in devices:
                if device[self._fields['fields'][5]]=='Wi-Fi Client' and initialTime['kismet.system.timestamp.sec'] - device[self._fields['fields'][6]] < time :
                    clients.append(device)
            return clients
        except:
            raise IPError('Wrong IP')

    def findDevices(self, devices, field, find):
        for device in devices:
            if device[field]==find:
                return device
    
    def filterFields(self, devices, field):
        listDev = []
        for device in devices:
            listDev.append(device[field])
        return listDev

    def calcDistanceAccurate(self, macAddr, accuracy): # recommended for Access Point
        RSSI = []
        while(len(RSSI) < accuracy):
            lastVal = self.getDeviceByMAC(macAddr)[0]['kismet.common.signal.last_signal']
            if self._triggerPacks(RSSI, lastVal):
                RSSI.append(lastVal)
        power = arithmeticMean(RSSI)
        return(self.calcDistanceIstant(power))
    
    def calcDistanceIstant(self, power):
        distance = pow(10, (self._A-power)/self._K)
        return truncate(distance, 3)

    def _triggerPacks(self, values, lastVal):
        if not values:
            return True
        else:
            if values[-1] == lastVal:
                return False
            else:
                return True
