import math, numpy, scipy.optimize

def arithmeticMean(values):
    tot = 0
    for value in values:
        tot += value
    return tot/len(values)

def quadraticMean(values):
    tot = 0
    for value in values:
        tot += pow(value, 2)
    mean = -pow(tot/len(values), 1/2)
    return mean

def truncate(n, decimals=0):
    multiplier = 10 ** decimals
    return int(n * multiplier) / multiplier

def convertIntoGhz(value):
    frequency = value*10**-6
    return truncate(frequency, 3)

def localize(x1,y1,z1,r1,x2,y2,z2,r2,x3,y3,z3,r3):
    sfera1 = (x-x1)**2 + (y-y1)**2 + (z-z1)**2 - r1**2
    sfera2 = (x-x2)**2 + (y-y2)**2 + (z-z2)**2 - r2**2
    sfera3 = (x-x3)**2 + (y-y3)**2 + (z-z3)**2 - r3**2
    