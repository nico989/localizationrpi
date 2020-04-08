from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox
from device import Device
from exception import IPError

class Interface(Frame):
    def __init__(self):
        super().__init__()
        self.master.title('DEVICE VIEWS')
        self.master.geometry('1200x600')
        self.master.rowconfigure(0, weight=1)
        self.master.columnconfigure(0, weight=1)
        self.grid(sticky=N+S+W+E)    
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
        self._tv = Treeview(self)
        self._tv['columns'] = ('mac', 'channel', 'frequency', 'rssi', 'distance') 
        self._labelName = ['Mac address', 'Channel', 'Frequency [Hz]', 'RSSI', 'Distance [m]']
        self._tv.heading('#0', text='Manufacturer', anchor='w')
        self._tv.column('#0', anchor='center', minwidth=120)     
        for index, name in enumerate(self._tv['columns']):
            self._tv.heading(name, text=self._labelName[index], anchor='center')
            self._tv.column(name, anchor='center', minwidth=120)
        self._tv.grid(row=0, column=0, sticky = (N,S,W,E))

    def _button(self):
        self._buttonPane = Frame(self)
        self._buttonPane.grid(row=1, column=0, sticky=W+E)

        Style().configure('TButton', background='#808080')

        self._inOut = StringVar()
        self._inOut.set('INDOOR')

        self._ipScanButton = Button(self._buttonPane, text='IP SCAN', takefocus=False, command=self._ipScan)
        self._ipScanButton.grid(row=0, column=0, padx=10, sticky=E)
        self._macSearchButton = Button(self._buttonPane, text='MAC SEARCH', takefocus=False, command=self._macSearch)
        self._macSearchButton.grid(row=0, column=2, padx=10, sticky=E)
        self._localizeButton = Button(self._buttonPane, text='LOCALIZE', takefocus=False)
        self._localizeButton.grid(row=0, column=4)
        self._indoorOutdoorButton = Button(self._buttonPane, textvariable=self._inOut, takefocus=False, command=self._indoorOutdoor)
        self._indoorOutdoorButton.grid(row=0, column=5)
        self._cleanAllButton = Button(self._buttonPane, text='CLEAN ALL', takefocus=False, command=self._cleanAll)
        self._cleanAllButton.grid(row=0, column=6)
    
    def _entryArea(self):
        self._ip = StringVar()
        self._ipEntry = Entry(self._buttonPane, textvariable=self._ip)
        self._ipEntry.grid(row=0, column=1, sticky=W)
        self._mac = StringVar()
        self._macEntry = Entry(self._buttonPane, textvariable=self._mac)
        self._macEntry.grid(row=0, column=3, sticky=W)

    def _label(self):
        self._product = Label(self._buttonPane, text=u'\u00A9 Product by Vinci Nicolò', font=('Comic Sans MS', 8))
        self._product.grid(row=0, column=7, sticky=SE)

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
                                                                  device[self._filterFields[3]], device[self._filterFields[4]]))
        except IPError as ip:
           messagebox.showerror(title='ERROR', message=ip)

    def _macSearch(self):
        for item in self._tv.get_children():
           if (self._tv.item(item, 'values')[0]) == self._macEntry.get():
               text = self._tv.item(item, 'text')
               values = self._tv.item(item, 'values')
               self._cleanAll()
               self._tv.insert('', 'end', iid=0, text=text, values=values)
               return
        messagebox.showerror(title='ERROR', message='It does not find')

    def _cleanAll(self):
        self._tv.delete(*self._tv.get_children())

    def _indoorOutdoor(self):
        if self._inOut.get() == 'INDOOR':
            self._device.setOutdoor()
            self._inOut.set('OUTDOOR')
        elif self._inOut.get() == 'OUTDOOR':
            self._device.setIndoor()
            self._inOut.set('INDOOR')
