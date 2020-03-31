import matplotlib.pyplot as plt
import numpy

class Plot:
    def __init__(self, title, xLabel, yLabel):
        self._xLabel = xLabel
        self._yLabel = yLabel
        self._title = title
    
    def line(self, inf, interval, sup, m, q):
        plt.xLabel = self._xLabel
        plt.yLabel = self._yLabel
        plt.title = self._title
        x = numpy.arange(inf, interval, sup)
        y = m*x + q
        plt.plot(x, y, color='black')
        plt.show()
    
    def points(self, valueX, valueY):
        plt.xLabel = self._xLabel
        plt.yLabel = self._yLabel
        plt.title = self._title
        plt.scatter(valueX, valueY, color='green', marker='*', s=30) 
        plt.show()

    def pointsAndLine(self, valueX, valueY, inf, interval, sup, m, q):
        plt.xLabel = self._xLabel
        plt.yLabel = self._yLabel
        plt.title = self._title
        x = numpy.arange(inf, interval, sup)
        y = m*x + q
        plt.plot(x, y, color='black')
        plt.scatter(valueX, valueY, color='green', marker='*', s=30) 
        plt.show()
  