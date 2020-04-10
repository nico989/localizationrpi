import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
from device import Device
from exception import IPError
from mathOperation import convertIntoGhz

class DevicePage(tk.Frame):
    def __init__(self, controller):
        tk.Frame.__init__(self)
        self._controller = controller
        self._controller.title('DEVICE VIEWS')
        self._controller.geometry('1200x600')
        self._controller.rowconfigure(0, weight=1)
        self._controller.columnconfigure(0, weight=1)
        self.grid(sticky='N'+'S'+'W'+'E') 
        self._filterFields = ['kismet.device.base.manuf',            
                              'kismet.device.base.macaddr',                              
                              'kismet.device.base.channel',
                              'kismet.device.base.frequency',
                              'kismet.common.signal.last_signal']
        self._table()
        self._button()
        self._entryArea()
        self._label()
        self._resizable()
        self._device = Device()

    def _table(self):
        self._tv = ttk.Treeview(self)
        self._tv['columns'] = ('mac', 'channel', 'frequency', 'rssi', 'distance') 
        self._labelName = ['Mac address', 'Channel', 'Frequency [GHz]', 'RSSI', 'Distance [m]']
        self._tv.heading('#0', text='Manufacturer', anchor='w')
        self._tv.column('#0', anchor='center', minwidth=120)     
        for index, name in enumerate(self._tv['columns']):
            self._tv.heading(name, text=self._labelName[index], anchor='center')
            self._tv.column(name, anchor='center', minwidth=120)
        self._tv.grid(row=0, column=0, sticky = ('N','S','W','E'))

    def _button(self):
        self._buttonPane = tk.Frame(self)
        self._buttonPane.grid(row=1, column=0, sticky='W'+'E')

        ttk.Style().configure('TButton', background='#808080')

        self._inOut = tk.StringVar()
        self._inOut.set('INDOOR')

        self._ipScanButton = ttk.Button(self._buttonPane, text='IP SCAN', takefocus=False, command=self._ipScan)
        self._ipScanButton.grid(row=0, column=0, padx=10, sticky='E')
        self._macSearchButton = ttk.Button(self._buttonPane, text='MAC SEARCH', takefocus=False, command=self._macSearch)
        self._macSearchButton.grid(row=0, column=2, padx=10, sticky='E')
        self._localizeButton = ttk.Button(self._buttonPane, text='LOCALIZE', takefocus=False, command=lambda: self._controller.show_frame('LocalizePage'))
        self._localizeButton.grid(row=0, column=4)
        self._indoorOutdoorButton = ttk.Button(self._buttonPane, textvariable=self._inOut, takefocus=False, command=self._indoorOutdoor)
        self._indoorOutdoorButton.grid(row=0, column=5)
        self._cleanAllButton = ttk.Button(self._buttonPane, text='CLEAN ALL', takefocus=False, command=self._cleanAll)
        self._cleanAllButton.grid(row=0, column=6)
    
    def _entryArea(self):
        self._ip = tk.StringVar()
        self._ipEntry = ttk.Entry(self._buttonPane, textvariable=self._ip)
        self._ipEntry.grid(row=0, column=1, sticky='W')
        self._mac = tk.StringVar()
        self._macEntry = ttk.Entry(self._buttonPane, textvariable=self._mac)
        self._macEntry.grid(row=0, column=3, sticky='W')

    def _label(self):
        self._product = ttk.Label(self._buttonPane, text=u'\u00A9 Product by Vinci Nicolò', font=('Comic Sans MS', 8))
        self._product.grid(row=0, column=7, sticky='SE')

    def _resizable(self):
        self.rowconfigure(0, weight=50)
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)
        for x in range(8):
            self._buttonPane.columnconfigure(x, weight=1)

    def _ipScan(self):
        try:
            self._cleanAll()
            self._device.setIp(self._ipEntry.get())
            devices = self._device.getClients()
            for index,device in enumerate(devices):
                self._tv.insert('', 'end', iid=index, text=device[self._filterFields[0]], values=(device[self._filterFields[1]], device[self._filterFields[2]], 
                                                                  convertIntoGhz(device[self._filterFields[3]]), device[self._filterFields[4]], 
                                                                  self._device.calcDistanceIstant(device[self._filterFields[4]])))
        except IPError as ip:
           tk.messagebox.showerror(title='ERROR', message=ip)

    def _macSearch(self):
        for item in self._tv.get_children():
           if (self._tv.item(item, 'values')[0]) == self._macEntry.get():
               text = self._tv.item(item, 'text')
               values = self._tv.item(item, 'values')
               self._cleanAll()
               self._tv.insert('', 'end', iid=0, text=text, values=values)
               return
        tk.messagebox.showerror(title='ERROR', message='It does not find')

    def _indoorOutdoor(self):
        if self._inOut.get() == 'INDOOR':
            self._device.setOutdoor()
            self._inOut.set('OUTDOOR')
        elif self._inOut.get() == 'OUTDOOR':
            self._device.setIndoor()
            self._inOut.set('INDOOR')

    def _cleanAll(self):
        self._tv.delete(*self._tv.get_children())
