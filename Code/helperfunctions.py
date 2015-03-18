from math import ceil,sqrt

################################################################################
### Helper Functions
################################################################################
def getEuclideanDist(start,end):
    x_s = start[0]
    y_s = start[1]
    x_e = end[0]
    y_e = end[1]

    return sqrt(pow(x_s-x_e,2)+pow(y_e-y_s,2))

def getManhattanDist(start,end):
    x_s = start[0]
    y_s = start[1]
    x_e = end[0]
    y_e = end[1]

    return (abs(x_s-x_e)+abs(y_e-y_s))

def getPathLength(path):
    dist = 0
    for i in range(len(path)-1):
        dist += getEuclideanDist(path[i],path[i+1])
    return dist
