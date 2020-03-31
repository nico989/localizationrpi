import numpy, math

class Regression:
    def __init__(self):
        self._distance = [0.5, 1, 2, 3, 4, 5]
        self._distanceLog = math.log10(self._distance)
        self._RSSIAritmetica = []
        self._RSSIQuadratica = []
    
    def addDistance(self, distance):
        self._distance.append(distance)
    
    def addRSSI(self, values):
        self._RSSIAritmetica.append(self._mediaAritmetica(values))
        self._RSSIQuadratica.append(-self._mediaQuadratica(values))

    def linearRegression(self):
        alphaA = numpy.cov(self._distanceLog, self._RSSIAritmetica)[0][1] /numpy.var(self._distanceLog)
        betaA = self._mediaAritmetica(self._RSSIAritmetica) - alphaA*self._mediaAritmetica(self._distanceLog)
        alphaQ = numpy.cov(self._distanceLog, self._RSSIQuadratica)[0][1] /numpy.var(self._distanceLog)
        betaQ = self._mediaAritmetica(self._RSSIQuadratica) - alphaQ*self._mediaAritmetica(self._distanceLog)
        result = [
            {
                "arithmeticK" : alphaA,
                "arithmeticA" : betaA
            },
            {
                "quadraticK" : alphaQ,
                "quadraticA" : betaQ
            }
        ]
        return result

    def _mediaAritmetica(self, val):
        tot = 0
        for value in val:
            tot += value
        media = tot/len(val)
        return self._truncate(media, 3)
    
    def _mediaQuadratica(self, val):
        tot = 0
        for value in val:
            tot += pow(value, 2)
        media = pow(tot/len(val), 1/2)
        return self._truncate(media, 3)

    def _truncate(self, n, decimals=0):
        multiplier = 10 ** decimals
        return int(n * multiplier) / multiplier
