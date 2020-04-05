from tkinter import *
from tkinter import messagebox
from device import Device
from exception import IPError

class Interface(Frame):
    def __init__(self):
        Frame.__init__(self)
        self.master.title('DEVICE VIEWS')
        self.master.geometry('1200x600')
        self.master.rowconfigure(0, weight=1)
        self.master.columnconfigure(0, weight=1)
        self.grid(sticky=N+S+W+E)    
        self._ipVar = StringVar()
        self.__listbox = []
        self._filterFields = ['kismet.device.base.macaddr',
                              'kismet.device.base.manuf',
                              'kismet.device.base.channel',
                              'kismet.device.base.frequency',
                              'kismet.common.signal.last_signal']
        self._upLabel()
        self._upListBox()
        self._upButton()
        self._upEntryArea()
        self._resizable()

    def _upLabel(self):
        _labelName = ['Mac address', 'Manufacturer', 'Channel', 'Frequency [Hz]', 'RSSI', 'Distance [m]']
        _listLabel = []
        for label in range(6):
            _listLabel.append(Label(self, text=_labelName[label], font=('Helvetica', 10), pady=5))
            _listLabel[label].grid(row=0, column=label, sticky=N+S+W+E)
        _product = Label(self, text=u'\u00A9 Product by Vinci Nicolò', font=('Comic Sans MS', 8))
        _product.grid(row=2, column=5, padx=10, pady=5, sticky=SE)
        
    def _upListBox(self):
        for lis in range(6):
            self.__listbox.append(Listbox(self, bg='lightgray', xscrollcommand=True, yscrollcommand=True))
            self.__listbox[lis].grid(row=1, column=lis, padx=10, sticky=N+S+W+E)
    
    def _upEntryArea(self):
        _ipArea = Entry(self, textvariable=self._ipVar, bg='#C0C0C0')
        _ipArea.grid(row=2, column=1, padx=10, pady=5, sticky=W)

    def _upButton(self):
        _scan = Button(self, text='Insert IP and scan', bg='#808080', command=self._printDev)
        _scan.grid(row=2, column=0, padx=10, pady=5, sticky=E)
        _clean = Button(self, text='Clean all', bg='#808080', command=self._cleanAll)
        _clean.grid(row=2, column=2, pady=5, sticky=W)

    def _resizable(self):
        self.rowconfigure(1, weight=50)
        self.rowconfigure(2, weight=1)
        for column in range(6):
            self.columnconfigure(column, weight=1)

    def _printDev(self):
        try:
            dev = Device(self._ipVar.get())
            clients = dev.getClients()
            for box in range (5):
                shows = dev.filterFields(clients, self._filterFields[box])
                for show in shows:
                    self.__listbox[box].insert(END, show)
            for s in shows:
                self.__listbox[5].insert(END, dev.calcDistanceIstant(s))
        except IPError as ip:
            messagebox.showerror(title='ERROR', message=ip)

    def _cleanAll(self):
        for box in range(6):
            self.__listbox[box].delete(0, END)
