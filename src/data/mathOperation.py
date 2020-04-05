def arithmeticMean(values):
    tot = 0
    for value in values:
        tot += value
    return tot/len(values)
    
def truncate(n, decimals=0):
    multiplier = 10 ** decimals
    return int(n * multiplier) / multiplier