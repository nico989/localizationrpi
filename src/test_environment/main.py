from collectData import CollectData
from regression import Regression
from plot import Plot

def main():
     data = CollectData('192.168.1.69', 'AC:75:1D:57:8A:D8')
     regression = Regression()
     value = input('Would you like to collect data? [y/n] ')
     n = 0
     while(value == 'y' and n<6):
          val = data.collect() # collect data foreach distance
          regression.addRSSI(val) # call AddRSSI of regression
          print(regression._RSSIAritmetica)
          print(regression._RSSIQuadratica)
          value = input('Would you still like to collect data?[y/n] ')
          n += 1
     result = regression.linearRegression() # call regression
     print(result)
     p1 = Plot('DEVICE', '-log10(distance)', 'RSSI') # plot line above point with datas gave from regression
     p1.pointsAndLine(regression.getLog10Distance(), regression.getRSSIAritmetica(), -1, 1, 100, result[0]['arithmeticK'], result[0]['arithmeticA'])

if __name__=="__main__":
    main()
