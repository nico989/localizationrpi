from req import Req
from tkinter import messagebox
from exception import HTTPError, IPError

class Device:
    def __init__(self, ipAddr):
        self._req = Req(ipAddr)
        self._fields = {'fields': [ 'kismet.device.base.macaddr',
                                    'kismet.device.base.manuf',
                                    'kismet.device.base.channel',
                                    'kismet.device.base.frequency',
                                    'kismet.device.base.signal/kismet.common.signal.last_signal',
                                    'kismet.device.base.type'
                                    #'kismet.device.base.first_time', # timpestamp della prima volta che ho visto il dispositivo
                                    #'kismet.device.base.last_time', # timpestamp dell'ultima volta che ho visto il dispositivo
                                    #'kismet.device.base.commonname'
                                    ]}

    def getAll(self):
        try:
            return self._req.post('/devices/views/phy-IEEE802.11/devices.json', self._fields)
        except HTTPError as error:
            messagebox.showerror(title='ERROR', message=error)
        except:
            raise IPError('Wrong IP')
        
    def getAccessPoint(self):
        try:
            return self._req.post('/devices/views/phydot11_accesspoints/devices.json', self._fields)
        except HTTPError as error:
            messagebox.showerror(title='ERROR', message=error)
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
        except HTTPError as error:
            messagebox.showerror(title='ERROR', message=error)
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