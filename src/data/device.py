from req import Req
from exception import HTTPError

class Device:
    def __init__(self, ipAddr):
        self.__req = Req(ipAddr)
        self.__fields = {'fields': ['kismet.device.base.commonname',
                                    'kismet.device.base.channel',
                                    'kismet.device.base.signal/kismet.common.signal.last_signal',
                                    'kismet.device.base.name',
                                    'kismet.device.base.macaddr',
                                    'kismet.device.base.type',
                                    # 'kismet.device.base.first_time' # timpestamp della prima volta che ho visto il dispositivo
                                    # 'kismet.device.base.last_time' # timpestamp dell'ultima volta che ho visto il dispositivo
                                    'kismet.device.base.frequency'
                                    ]}
        self.__devices = []

    def get(self, path):
        try:
            self.__devices = self.__req.post('/devices/views/' +  path + '/devices.json', self.__fields)
            return self.__devices
        except HTTPError as error:
            return error

    def find(self, fields, filt):
        listDev = []
        for dev in self.__devices:
            if(dev[fields] == filt):
                listDev.append(dev)
        return listDev
    
    def filter(self, fields):
        listDev = []
        for dev in self.__devices:
            for x in fields:
                listDev.append(dev[x])
        return listDev
