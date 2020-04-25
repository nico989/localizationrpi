from device import Device
import tkinter as tk  
import tkinter.ttk as ttk
import matplotlib, numpy
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
from mpl_toolkits.mplot3d import Axes3D
from mathOperation import localize

class LocalizePage(tk.Frame):
    def __init__(self, controller):
        tk.Frame.__init__(self)
        self._controller = controller
        self._controller.rowconfigure(0, weight=1)
        self._controller.columnconfigure(0, weight=1)
        self.grid(sticky='N'+'S'+'W'+'E')
        self._filterFields = ['kismet.device.base.macaddr', 'kismet.common.signal.last_signal']
        self._device = Device()    
        self._distances = {1:1, 2:1, 3:1} 
        self._initialPositions = [(0,0,0), (1,0,0), (1,1,0)]
        self._graph()     
        self._button()
        self._entryArea()
        self._label()
        self._resizable()
    
    def setIPAddr(self, value):
        self._device.setIP(value)

    def _graph(self):
        self._figure = Figure(figsize=(5,5), dpi=150)
        
        self._canvas = FigureCanvasTkAgg(self._figure, self)       
        self._canvas.draw()

        self._subplot = self._figure.add_subplot(111, projection='3d')
        
        self._toolbarFrame = tk.Frame(self)
        self._toolbarFrame.grid(row=1, column=0, sticky='W')
        self._toolbar = NavigationToolbar2Tk(self._canvas, self._toolbarFrame)
        self._toolbar.update()

    def _button(self):
        self._buttonPane = tk.Frame(self)
        self._buttonPane.grid(row=2, column=0, sticky='W'+'E')

        ttk.Style().configure('TButton', background='#808080')

        self._saveIPButton = ttk.Button(self._buttonPane, text='SAVE IP', takefocus=False, command=lambda: self._saveIP())
        self._saveIPButton.grid(row=0, column=0, padx=10, pady=10, sticky='E')
        self._locMacLabel = tk.StringVar()
        self._locMacLabel.set('LOCALIZE FROM MAC ADDRESS')
        self._locMacButton = ttk.Button(self._buttonPane, textvariable=self._locMacLabel, takefocus=False, command=lambda: self._getPosByMAC())
        self._locMacButton.grid(row=0, column=2, padx=10, pady=10, sticky='E')
        self._locAllLabel = tk.StringVar()
        self._locAllLabel.set('LOCALIZE ALL POSSIBLE DEVICES')       
        self._locAllButton = ttk.Button(self._buttonPane, textvariable=self._locAllLabel, takefocus=False, command=lambda: self._fillGraph())
        self._locAllButton.grid(row=0, column=4, padx=10, pady=10, sticky='E')
        self._returnToDevicePage = ttk.Button(self._buttonPane, text='GO TO DEVICE PAGE', takefocus=False, command=lambda: self._controller.showFrame('DevicePage'))
        self._returnToDevicePage.grid(row=0, column=6, padx=10, pady=10)

    def _entryArea(self):
        self._mac = tk.StringVar()
        self._macEntry = ttk.Entry(self._buttonPane, textvariable=self._mac)
        self._macEntry.grid(row=0, column=3, pady=10, sticky='W')
        self._ip = tk.StringVar()
        self._ipEntry = ttk.Entry(self._buttonPane, textvariable=self._ip)
        self._ipEntry.grid(row=0, column=1, pady=10, sticky='W')
        self._locAll = tk.StringVar()
        self._locAllEntry = ttk.Entry(self._buttonPane, textvariable=self._locAll)
        self._locAllEntry.grid(row=0, column=5, pady=10, sticky='W')

    def _label(self):
        self._product = ttk.Label(self._buttonPane, text=u'\u00A9 Product by Vinci Nicolò', font=('Comic Sans MS', 8))
        self._product.grid(row=0, column=7, pady=10, sticky='SE')
        
    def _resizable(self):
        self.rowconfigure(0, weight=50)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.columnconfigure(0, weight=1)
        for x in range(8):
            self._buttonPane.columnconfigure(x, weight=1)

    def _saveIP(self):
        self._device.setIP(self._ipEntry.get())

    #TODO THREAD
    def _getPosByMAC(self):
        macAddr = ''
        task = self._updateLabel(self._locMacLabel, 'LOCALIZE FROM MAC ADDRESS')
        if task is None:
            macAddr = self._macEntry.get()
        elif task == 4:
            result = localize(self._initialPositions[0][0], self._initialPositions[0][1], self._initialPositions[0][2], self._distances[1],
                                        self._initialPositions[1][0], self._initialPositions[1][1], self._initialPositions[1][2], self._distances[2],
                                        self._initialPositions[2][0], self._initialPositions[2][1], self._initialPositions[2][2], self._distances[3]
                                        )
            if result is None:
                tk.messagebox.showinfo(title='INFO', message='It does not find real points')
            else:
                self._displayGraph(result['radius'], result['meanPoint'], result['points'], self._initialPositions)
            self._initialPositions.clear()
        else:           
            '''initPos = self._macEntry.get().split(',')
            initPos = [int(i) for i in initPos] 
            self._initialPositions.append(tuple(initPos))
            distance = self._device.calcDistanceAccurate(macAddr, 20)
            if distance:
                self._distances[task] = distance
            else:
                tk.messagebox.showerror(title='Error', message='MAC address is not correct')'''                                  
       
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

    def _displayGraph(self, radius, centerPoint, points, initialPoints):
        self._subplot.clear()       
        
        scatter1 = self._subplot.scatter(points[0], points[1], points[2], color='red', marker='^')
        for initial in initialPoints:
            xInit = initial[0]
            yInit = initial[1]
            zInit = initial[2]
            scatter2 = self._subplot.scatter(xInit, yInit, zInit, color='blue', marker='o')

        scatter3 = self._subplot.scatter(centerPoint[0], centerPoint[1], centerPoint[2], color='green', marker='o')
        u = numpy.linspace(0, 2 * numpy.pi, 100)
        v = numpy.linspace(0, numpy.pi, 100)
        x = radius * (numpy.outer(numpy.cos(u), numpy.sin(v)) + centerPoint[0])
        y = radius * (numpy.outer(numpy.sin(u), numpy.sin(v)) + centerPoint[1])
        z = radius * (numpy.outer(numpy.ones(numpy.size(u)), numpy.cos(v)) + centerPoint[2])
        surface1 = self._subplot.plot_surface(x, y, z, rstride=1, cstride=1, color='lightblue', shade=0, alpha=0.5)

        self._subplot.set_xlabel('x axis')
        self._subplot.set_ylabel('y axis')
        self._subplot.set_zlabel('z axis')
        self._subplot.set_xlim(min(points[0]) - 1, max(points[0]) + 1)
        self._subplot.set_ylim(max(points[1]) + 1, min(points[1]) - 1)
        self._subplot.set_zlim(min(points[2]) - 1, max(points[2]) + 1)
        self._subplot.xaxis._axinfo['juggled'] = (0,0,0)
        self._subplot.yaxis._axinfo['juggled'] = (1,1,1)
        self._subplot.zaxis._axinfo['juggled'] = (2,2,2)

        self._subplot.legend([scatter1, scatter2, scatter3], ['Probable points', 'Initial points', 'Center of area'])

        self._canvas.get_tk_widget().grid(row=0, column=0, sticky='N'+'S'+'W'+'E')     
