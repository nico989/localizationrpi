from device import Device
import tkinter as tk  
import tkinter.ttk as ttk
import matplotlib, numpy, threading
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
from mpl_toolkits.mplot3d import Axes3D
from mathOperation import localize, distanceBetweenTwoPoints, truncate
from exception import ConnError

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
        self._macAddr = '' #D8:CE:3A:F4:C5:19
        self._check = True
        self._graph()     
        self._button()
        self._entryArea()
        self._label()
        self._resizable()
        self._getInitialPositions()

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

        self._save = tk.StringVar()
        self._save.set('SAVE IP')
        self._saveIPButton = ttk.Button(self._buttonPane, textvariable=self._save, takefocus=False, command=lambda: self._saveIP())
        self._saveIPButton.grid(row=0, column=0, padx=10, pady=10, sticky='E')
        self._locMacLabel = tk.StringVar()
        self._locMacLabel.set('GET FIRST POSITION')
        self._locMacButton = ttk.Button(self._buttonPane, textvariable=self._locMacLabel, takefocus=False, command=lambda: self._getPosByMAC())
        self._locMacButton.grid(row=0, column=2, padx=10, pady=10)
        self._returnToDevicePageButton = ttk.Button(self._buttonPane, text='GO TO DEVICE PAGE', takefocus=False, command=lambda: self._returnToDevicePage())
        self._returnToDevicePageButton.grid(row=0, column=3, padx=10, pady=10)

    def _entryArea(self):
        self._ipMac = tk.StringVar()
        self._ipMacEntry = ttk.Entry(self._buttonPane, textvariable=self._ipMac)
        self._ipMacEntry.grid(row=0, column=1, pady=10, sticky='W')

    def _label(self):
        self._product = ttk.Label(self._buttonPane, text=u'\u00A9 Product by Vinci Nicolò', font=('Comic Sans MS', 8))
        self._product.grid(row=0, column=4, pady=10, sticky='SE')
        
    def _resizable(self):
        self.rowconfigure(0, weight=50)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.columnconfigure(0, weight=1)
        for x in range(5):
            self._buttonPane.columnconfigure(x, weight=1)
    
    def _getInitialPositions(self):
        self._initialPositions = []
        self._initPointsFile = open('initialPoints.txt', 'r')
            for line in self._initPointsFile.readlines():
                point = tuple(map(int, line.strip('\r\n').split(',')))
                self._initialPositions.append(point)

    def _saveIP(self):
        if self._saveLabel.get() == 'SAVE IP':
            self._device.setIP(self._ipMacEntry.get())
            self._saveLabel.set('SAVE MAC')
        elif self._saveLabel.get() == 'SAVE MAC':
            self._macAddr = self._ipMacEntry.get()
            self._saveLabel.set('SAVE IP')

    def _returnToDevicePage(self):
        self._resetMac()
        self._controller.showFrame('DevicePage')

    def _posThread(self):
        if self._check:
            threading.Thread(target= self._getPosByMAC, daemon=True).start()
        else:
            tk.messagebox.showerror(title='ERROR', message='Another thread is running')

    def _getPosByMAC(self):
        try:
            self._check = False            
            if self._updateLabel():
                distance = self._device.calcDistanceAccurate(self._macAddr, 20)
                if distance is not None:
                    self._distances[task] = distance
                    print(self._distances)
                else:
                    tk.messagebox.showerror(title='Error', message='MAC address is not correct')
            else:
                result = localize(self._initialPositions[0][0], self._initialPositions[0][1], self._initialPositions[0][2], self._distances[1],
                                            self._initialPositions[1][0], self._initialPositions[1][1], self._initialPositions[1][2], self._distances[2],
                                            self._initialPositions[2][0], self._initialPositions[2][1], self._initialPositions[2][2], self._distances[3]
                                            )
                if result is None:
                    tk.messagebox.showinfo(title='INFO', message='It does not find real points')
                else:
                    self._displayGraph(result['radius'], result['meanPoint'], result['points'], self._initialPositions)
                self._initialPositions.clear()      
        except ConnError as conn:
            self._resetMac()
            tk.messagebox.showerror(title='ERROR', message=conn)
        finally:
            self._check = True
    
    def _resetMac(self):
        self._locMacLabel.set('LOCALIZE FROM MAC ADDRESS')
        self._initialPositions.clear()                                  
       
    def _updateLabel(self):
        if self._locMacLabel.get() == 'GET FIRST POSITION':
            self._locMacLabel.set('GET SECOND POSITION')
            return True
        elif self._locMacLabel.get() == 'GET SECOND POSITION':
            self._locMacLabel.set('GET THIRD POSITION')
            return True
        elif self._locMacLabel.get() == 'GET THIRD POSITION':
            self._locMacLabel.set('CALCULATE POSITION')
            return False
        elif self._locMacLabel.get() == 'CALCULATE POSITION':
            self._locMacLabel.set('GET FIRST POSITION')
            return True

    def _displayGraph(self, radius, centerPoint, points, initialPoints):
        self._subplot.clear()       
        
        scatter1 = self._subplot.scatter(points[0], points[1], points[2], color='red', marker='o')
        for initial in initialPoints:
            scatter2 = self._subplot.scatter(initial[0], initial[1], initial[2], color='blue', marker='o')
            self._subplot.plot([initial[0], centerPoint[0]], [initial[1], centerPoint[1]], [initial[2], centerPoint[2]], color='black')
            self._subplot.text(numpy.mean([initial[0],centerPoint[0]]), numpy.mean([initial[1],centerPoint[1]]), numpy.mean([initial[2],centerPoint[2]]), str(truncate(distanceBetweenTwoPoints(initial, centerPoint), 3)))

        scatter3 = self._subplot.scatter(centerPoint[0], centerPoint[1], centerPoint[2], color='green', marker='o')
        u = numpy.linspace(0, 2 * numpy.pi, 100)
        v = numpy.linspace(0, numpy.pi, 100)
        x = (radius * numpy.outer(numpy.cos(u), numpy.sin(v))) + centerPoint[0]
        y = (radius * numpy.outer(numpy.sin(u), numpy.sin(v))) + centerPoint[1]
        z = (radius * numpy.outer(numpy.ones(numpy.size(u)), numpy.cos(v))) + centerPoint[2]
        self._subplot.plot_surface(x, y, z, rstride=1, cstride=1, color='lightblue', shade=0, alpha=0.5)

        self._subplot.set_xlabel('x axis')
        self._subplot.set_ylabel('y axis')
        self._subplot.set_zlabel('z axis')
        self._subplot.set_xlim(min(points[0]) - 1, max(points[0]) + 1)
        self._subplot.set_ylim(max(points[1]) + 1, min(points[1]) - 1)
        self._subplot.set_zlim(min(points[2]) - 1, max(points[2]) + 1)
        self._subplot.xaxis._axinfo['juggled'] = (0,0,0)
        self._subplot.yaxis._axinfo['juggled'] = (1,1,1)
        self._subplot.zaxis._axinfo['juggled'] = (2,2,2)

        self._subplot.legend([scatter1, scatter2, scatter3], ['Probable points', 'Initial points', 'Center of area: '+str(centerPoint[0])+','+str(centerPoint[1])+','+str(centerPoint[2])])

        self._canvas.get_tk_widget().grid(row=0, column=0, sticky='N'+'S'+'W'+'E')     
