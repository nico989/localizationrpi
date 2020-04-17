from device import Device
from exception import IPError
import tkinter as tk  
import tkinter.ttk as ttk
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
#from matplotlib import Figure


class LocalizePage(tk.Frame):

    def __init__(self, controller, async_loop):
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
        self._device.setIp(value)

    def _graph(self):
        pass

    def _button(self):
        self._buttonPane = tk.Frame(self)
        self._buttonPane.grid(row=1, column=0, sticky='W'+'E')

        ttk.Style().configure('TButton', background='#808080')

        self._counterPos = tk.StringVar()
        self._counterPos.set('GET FIRST POSITION')

        self._locMacButton = ttk.Button(self._buttonPane, text='LOCALIZE FROM MAC ADDRESS', takefocus=False)
        self._locMacButton.grid(row=0, column=0, padx=10, pady=5, sticky='E')       
        self._getPosButton = ttk.Button(self._buttonPane, textvariable=self._counterPos, takefocus=False, command=self._getPos)
        self._getPosButton.grid(row=0, column=2, padx=10, pady=5)
        self._locAll = ttk.Button(self._buttonPane, text='LOCALIZE ALL POSSIBILE DEVICE', takefocus=False)
        self._locAll.grid(row=0, column=3, padx=10, pady=5)
        self._returnToDevicePage = ttk.Button(self._buttonPane, text='GO TO DEVICE PAGE', takefocus=False, command=lambda: self._controller.showFrame('DevicePage'))
        self._returnToDevicePage.grid(row=0, column=4, padx=10, pady=5)

    def _entryArea(self):
        self._mac = tk.StringVar()
        self._macEntry = ttk.Entry(self._buttonPane, textvariable=self._mac)
        self._macEntry.grid(row=0, column=1, pady=5, sticky='W')

    def _label(self):
        self._product = ttk.Label(self._buttonPane, text=u'\u00A9 Product by Vinci Nicolò', font=('Comic Sans MS', 8))
        self._product.grid(row=0, column=5, pady=5, sticky='SE')
        
    def _resizable(self):
        self.rowconfigure(0, weight=1)
        #self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)
        for x in range(6):
            self._buttonPane.columnconfigure(x, weight=1)

    #TODO ASYNC
    def _getPos(self):
        try:
            if self._counterPos.get() == 'GET FIRST POSITION':
                index = 'first'
                self._counterPos.set('GET SECOND POSITION')
            elif self._counterPos.get() == 'GET SECOND POSITION':
                index = 'second'
                self._counterPos.set('GET THIRD POSITION')
            elif self._counterPos.get() == 'GET THIRD POSITION':
                index = 'third'
                self._counterPos.set('CALCULATE POSITION')
            elif self._counterPos.get() == 'CALCULATE POSITION':
                index = ''
                self._counterPos.set('GET FIRST POSITION')
            if index == '':
                #TODO: calc positions con self._distances{}
                pass
            else:
                devices = self._device.getClients()
                distances = []
                for device in devices:
                    distances.append(self._device.calcDistanceAccurate(device, 20))
                self._distances[index] = distances
                  
        except IPError as error:
            tk.messagebox.showerror(title='Error', message=error)
