from device import Device
from exception import IPError
import tkinter as tk  
import tkinter.ttk as ttk
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
#from matplotlib import Figure


class LocalizePage(tk.Frame):

    def __init__(self, controller):
        tk.Frame.__init__(self)
        self._controller = controller
        self._controller.rowconfigure(0, weight=1)
        self._controller.columnconfigure(0, weight=1)
        self.grid(sticky='N'+'S'+'W'+'E')
        self._filterFields = ['kismet.device.base.macaddr', 'kismet.common.signal.last_signal']
        self._device = Device()    
        self._distances = {}      
        self._button()
        self._entryArea()
        self._label()
        self._resizable()
    
    def setIPAddr(self, value):
        self._device.setIP(value)

    def _graph(self):
        pass

    def _button(self):
        self._buttonPane = tk.Frame(self)
        self._buttonPane.grid(row=1, column=0, sticky='W'+'E')

        ttk.Style().configure('TButton', background='#808080')

        self._saveIPButton = ttk.Button(self._buttonPane, text='SAVE IP', takefocus=False, command=lambda: self._saveIP())
        self._saveIPButton.grid(row=0, column=0, padx=10, pady=5, sticky='E')
        self._locMacLabel = tk.StringVar()
        self._locMacLabel.set('LOCALIZE FROM MAC ADDRESS')
        self._locMacButton = ttk.Button(self._buttonPane, textvariable=self._locMacLabel, takefocus=False, command=lambda: self._getPosByMAC())
        self._locMacButton.grid(row=0, column=2, padx=10, pady=5, sticky='E')
        self._locAllLabel = tk.StringVar()
        self._locAllLabel.set('LOCALIZE ALL POSSIBLE DEVICES')       
        self._locAll = ttk.Button(self._buttonPane, textvariable=self._locAllLabel, takefocus=False)
        self._locAll.grid(row=0, column=4, padx=10, pady=5)
        self._returnToDevicePage = ttk.Button(self._buttonPane, text='GO TO DEVICE PAGE', takefocus=False, command=lambda: self._controller.showFrame('DevicePage'))
        self._returnToDevicePage.grid(row=0, column=5, padx=10, pady=5)

    def _entryArea(self):
        self._mac = tk.StringVar()
        self._macEntry = ttk.Entry(self._buttonPane, textvariable=self._mac)
        self._macEntry.grid(row=0, column=3, pady=5, sticky='W')
        self._ip = tk.StringVar()
        self._ipEntry = ttk.Entry(self._buttonPane, textvariable=self._ip)
        self._ipEntry.grid(row=0, column=1, pady=5, sticky='W')

    def _label(self):
        self._product = ttk.Label(self._buttonPane, text=u'\u00A9 Product by Vinci Nicolò', font=('Comic Sans MS', 8))
        self._product.grid(row=0, column=6, pady=5, sticky='SE')
        
    def _resizable(self):
        self.rowconfigure(0, weight=1)
        #self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)
        for x in range(7):
            self._buttonPane.columnconfigure(x, weight=1)

    def _saveIP(self):
        self._device.setIP(self._ipEntry.get())

    #TODO THREAD
    def _getPosByMAC(self):
        try:
            task = self._updateLabel(self._locMacLabel, 'LOCALIZE FROM MAC ADDRESS')
            if task:
                if task == 4:
                    #TODO:calc position
                    pass
                else:
                    device = self._device.getDeviceByMAC(self._macEntry.get())
                    if device:
                        self._distances[task] = self._device.calcDistanceAccurate(device[0], 20)                   
        except IPError as error:
            tk.messagebox.showerror(title='Error', message=error)

    def _updateLabel(self, variableLabel, initialValue):
        if variableLabel.get() == initialValue:
            variableLabel.set('GET FIRST POSITION')
            return 
        elif variableLabel.get() == 'GET FIRST POSITION':
            variableLabel.set('GET SECOND POSITION')
            return 1
        elif variableLabel.get() == 'GET SECOND POSITION':
            variableLabel.set('GET THIRD POSITION')
            return 2
        elif variableLabel.get() == 'GET THIRD POSITION':
            variableLabel.set('CALCULATE POSITION')
            return 3
        elif variableLabel.get() == 'CALCULATE POSITION':
            variableLabel.set(initialValue)
            return 4
