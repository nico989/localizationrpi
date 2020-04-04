from req import Req
from exception import IPError

class Device:
    def __init__(self, ipAddr):
        self._req = Req(ipAddr)
        self._fields = {'fields': [ 'kismet.device.base.macaddr',
                                    'kismet.device.base.manuf',
                                    'kismet.device.base.channel',
                                    'kismet.device.base.frequency',
                                    'kismet.device.base.signal/kismet.common.signal.last_signal',
                                    'kismet.device.base.type',
                                    'kismet.device.base.last_time'
                                    ]}
        self._K = 16.114
        self._A = -46.0141

    def getAll(self):
        try:
            return self._req.post('/devices/views/phy-IEEE802.11/devices.json', self._fields)
        except:
            raise IPError('Wrong IP')
        
    def getAccessPoint(self):
        try:
            return self._req.post('/devices/views/phydot11_accesspoints/devices.json', self._fields)
        except:
            raise IPError('Wrong IP')

    def getDeviceByMAC(self, macAddr):
            try:
                return self._req.post('/devices/by-mac/' + macAddr + '/devices.json', self._fields)
            except:
                raise IPError('Wrong IP')

    def getClients(self):
        try:
            clients = []
            devices = self._req.post('/devices/views/phy-IEEE802.11/devices.json', self._fields)
            for device in devices:
                if device['kismet.device.base.type']=='Wi-Fi Client':
                    clients.append(device)
            return clients
        except:
            raise IPError('Wrong IP')

    def getClientsLastTimeSec(self, time):
        try:
            clients = []
            initialTime = self._req.get('/system/timestamp.json', None)
            devices = self._req.post('/devices/views/phy-IEEE802.11/devices.json', self._fields)
            for device in devices:
                if device['kismet.device.base.type']=='Wi-Fi Client' and initialTime['kismet.system.timestamp.sec'] - device['kismet.device.base.last_time'] < time :
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

    def calcDistance(self, power):
        d = pow(10, (self._A-power)/self._K)
        return self._truncate(d, 3)
    
    ''' Value INDOOR
    def indoor(self):
        self._K = 
        self._A = 
    '''
    '''Value OUTDOOR
    def outdoor(self):
        self._K = 
        self._A =
    '''

    def _truncate(self, n, decimals=0):
        multiplier = 10 ** decimals
        return int(n * multiplier) / multiplier
