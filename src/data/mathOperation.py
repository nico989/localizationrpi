import math, sympy

def distanceBetweenTwoPoints(p1, p2):
    distance = pow((p1[0]-p2[0])**2+(p1[1]-p2[1])**2+(p1[2]+p2[2]**2), 1/2)
    return distance

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
    sympy.init_printing()
    x,y,z = sympy.symbols('x,y,z')
    sphere1 = sympy.Eq((x-x1)**2+(y-y1)**2+(z-z1)**2,r1**2)
    sphere2 = sympy.Eq((x-x2)**2+(y-y2)**2+(z-z2)**2,r2**2)
    sphere3 = sympy.Eq((x-x3)**2+(y-y3)**2+(z-z3)**2,r3**2)
    results = sympy.solve([sphere1,sphere2,sphere3],(x,y,z))
    print('Results:\n' + str(results))
    coordinates = ([], [], [])
    for result in results:
        for i in range(3):
            if result[i].is_real:
                approximateValue = truncate(result[i].evalf(), 3)
                coordinates[i].append(approximateValue)
            else:
                return
    print('All coordinates:\n' + str(coordinates))
    meanPoint = (arithmeticMean(coordinates[0]), arithmeticMean(coordinates[1]), arithmeticMean(coordinates[2]))
    print('Point coordinates: ' + str(meanPoint))
    allDistanceFromMeanPoint = []
    for result in results:
        allDistanceFromMeanPoint.append(distanceBetweenTwoPoints(meanPoint, result))
    print(allDistanceFromMeanPoint)
    radius = truncate(max(allDistanceFromMeanPoint), 3)
    print('Radius: ' + str(radius))
    res = {
        'radius': radius,
        'meanPoint': meanPoint,
        'points': coordinates
    }
    return res
