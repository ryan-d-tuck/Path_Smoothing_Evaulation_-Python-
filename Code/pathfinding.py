import pygame, sys, os
from collections import defaultdict
from math import ceil,sqrt

from constants import *
from helperfunctions import *

################################################################################
### WorldMap
################################################################################
class WorldMap:
    """ WorldMap is a one-to-one representation of the underlying worldspace. It
        is a uniform grid of points, with each point being either 'blocked' or
        'unblocked'.
    """
    def __init__(self, map_path=None, width=None, height=None):
        self._map       = dict()
        if(map_path):
            self.loadMap(map_path)
        elif(width and height):
            self.width  = width
            self.height = height

    def add(self,point):
        self._map[point] = True

    def remove(self,point):
        if point in self._map:
            self._map[point] = False

    def checkCell(self,point):
        if point in self._map:
            return self._map[point]
        else:
            return False

    def loadMap(self,map_path):
        f = open(map_path)

        num = 0
        line = f.readline()
        while line:
            if num == 1:
                temp = str.split(line," ",1)
                height = int(temp[1])
            elif num == 2:
                temp = str.split(line," ",1)
                width = int(temp[1])
            elif num >= 4:
                for i in range(width):
                    if(line[i] == '@'):
                        x       = i
                        y       = num - 4
                        self.add((x,y))
            num += 1
            line = f.readline()

        self.width = width
        self.height = height

    def getMap():
        return self._map

    def lineOfSight(self, p0, p1):
        x0 = p0[0]
        y0 = p0[1]
        x1 = p1[0]
        y1 = p1[1]
        points = []

        steep = (abs(y1 - y0) > abs(x1 - x0))
        switch = (x0 > x1)

        if (steep):
            x0, y0 = y0, x0
            x1, y1 = y1, x1

        deltax = abs(x1 - x0)
        deltay = abs(y1 - y0)
        error = 0
        y = y0
        if(y0 < y1):
            ystep = 1
        else:
            ystep = -1

        if(x0 < x1):
            xstep = 1
        else:
            xstep = -1

        for x in range(x0,x1,xstep):
            if (steep):
                if(self.checkCell((y,x))):
                    return False
            else:
                if(self.checkCell((x,y))):
                    return False

            error += deltay
            if (2 * error >= deltax):
                y += ystep
                error -= deltax

        return True

    def getCardinalPath(self, p0, p1):
        x0 = p0[0]
        y0 = p0[1]
        x1 = p1[0]
        y1 = p1[1]
        points = []

        steep = (abs(y1 - y0) > abs(x1 - x0))
        switch = (x0 > x1)

        if (steep):
            x0, y0 = y0, x0
            x1, y1 = y1, x1

        deltax = abs(x1 - x0)
        deltay = abs(y1 - y0)
        error = 0
        y = y0
        if(y0 < y1):
            ystep = 1
        else:
            ystep = -1

        if(x0 < x1):
            xstep = 1
        else:
            xstep = -1

        for x in range(x0,x1,xstep):
            if (steep):
                #print("Start: ", y,x)
                points.append((y,x))
            else:
                #print("Start: ", x,y)
                points.append((x,y))

            error += deltay
            if (2 * error >= deltax):
                y += ystep
                error -= deltax
            #print("End: ", x,y)

        return points

################################################################################
### ScenInfo
################################################################################
class ScenInfo:
    def __init__(self,scen_path):
        self.loadScen(scen_path)

    def loadScen(self,scen_path):
        self.records = []
        self.curr = 0

        f = open(scen_path)

        num = 0
        line = f.readline()
        while line:
            if num >= 1:
                temp = str.split(line," ")
                x0 = int(temp[4])
                y0 = int(temp[5])
                x1 = int(temp[6])
                y1 = int(temp[7])
                opt = float(temp[8])
                self.records.append({"x0":x0,"y0":y0,"x1":x1,"y1":y1,"opt":opt, "num":int(temp[0])})
                self.curr += 1
            num += 1
            line = f.readline()
        self.curr = 0

    def loadNum(self,num):
        for i in range(len(self.records)):
            if(self.records[i]['num'] == num):
                self.curr = i
                return

    def getCurrInd(self):
        return self.curr

    def getCurr(self):
        return self.records[self.curr]

    def getNext(self):
        self.curr += 1
        self.curr = self.curr%len(self.records)
        return self.getCurr()

    def getPrev(self):
        self.curr -= 1
        self.curr = self.curr%len(self.records)
        return self.getCurr()

################################################################################
### QuadTree
################################################################################

class QuadTreeNode():
    """ QuadTreeNode is a node of a quad tree. It takes in a WorldMap (or similar
        dict) and then creates mopre nodes, down to a specific depth.
    """
    def __init__(self, x, y, w, h, depth = -1, parent=None):
        self.x      = int(x)
        self.y      = int(y)
        self.w      = int(w)
        self.h      = int(h)
        self.depth  = int(depth + 1)
        self.parent = parent
        self.nodes  = None
        self.fill   = None

    def check(self,mapGrid):
        count = 0
        for i in range(self.x,self.x + self.w):
            for j in range(self.y,self.y + self.h):
                if(mapGrid.checkCell((i,j))):
                    count += 1
        if(count == 0):
            self.fill = QT_EMPTY
        elif(count == (self.w*self.h)):
            self.fill = QT_FULL
        else: #(count > 1 and count < (self.w*self.h))
            self.fill = QT_OPEN
            self.subdivide(mapGrid)
        return True

    def subdivide(self,mapGrid):
        if(self.depth >= QUAD_TREE_DEPTH):
            return

        self.nodes = dict()

        w = self.w / 2
        h = self.h / 2

        #Upper Left
        node = QuadTreeNode(self.x, self.y, w, h, self.depth, self)
        node.check(mapGrid)
        self.nodes["UL"] = node

        #Upper Right
        node = QuadTreeNode(self.x + w, self.y, w, h, self.depth, self)
        node.check(mapGrid)
        self.nodes["UR"] = node

        #Lower Left
        node = QuadTreeNode(self.x, self.y + h, w, h, self.depth, self)
        node.check(mapGrid)
        self.nodes["LL"] = node

        #Lower Right
        node = QuadTreeNode(self.x + w, self.y + h, w, h, self.depth, self)
        node.check(mapGrid)
        self.nodes["LR"] = node

    def getRect(self):
        return pygame.Rect(self.x,self.y,self.w,self.h)

    def getFlattened(self):
        rects = self._getFlattenedSub()

        for times in range(OPTIMIZE_QUADS):
            rectsCopy   = list(rects)
            rects       = []
            while rectsCopy:
                rect1 = rectsCopy.pop()
                combined = False
                for rect2 in rectsCopy:
                    rectU = rect1.union(rect2)                
                    if((rect1.w * rect1.h)+(rect2.w * rect2.h)==(rectU.w * rectU.h)):
                        rects.append(rectU)
                        rectsCopy.remove(rect2)
                        combined = True
                        break
                if not combined:
                    rects.append(rect1)
        return rects

    def _getFlattenedSub(self):
        rects = []
        if(self.nodes == None and self.fill == QT_EMPTY):
            rects.append(self.getRect())
        elif(self.nodes):
            for loc in ["UL","UR","LL","LR"]:
                if(loc in self.nodes):
                    rects.extend(self.nodes[loc]._getFlattenedSub())
                    
        return rects

################################################################################
### NavMap
################################################################################
class NavMap:
    """ NavMap is an adjacent list of nodes. It is created from a list of rects
        (gotten from a flattened and pruned quad tree).
    """
    def __init__(self, rects):
        self.adjList = dict(dict()) #self.adjList[loc][adjacent loc] = distance
        for rect in rects:
            tl = rect.topleft
            tr = rect.topright
            bl = rect.bottomleft
            br = rect.bottomright 

            for point in [tl, tr, bl, br]:
                if not(point in self.adjList):
                    self.adjList[point] = {}

                for adjPoint in [tl, tr, bl, br]:
                    if point != adjPoint:
                        self.adjList[point][adjPoint] = getEuclideanDist(point,adjPoint)

    def getClosest(self,point):
        #This function returns the closest node to a given point
        distRecord = INFINITY
        locRecord = None
        for loc in self.adjList.keys():
            dist = getEuclideanDist(point,loc)
            if(dist < distRecord):
                distRecord = dist
                locRecord = loc
        return locRecord

    def getAdjList(self,start,end):
        #Check if start and end are in the adjlist
        #   if they're not, find the closest points, add connection
        if not start in self.adjList:
            startClosest = self.getClosest(start)
            self.adjList[start] = {}
            self.adjList[start][startClosest] = getEuclideanDist(start,startClosest)
            self.adjList[startClosest][start] = getEuclideanDist(startClosest,start)
        if not end in self.adjList:
            endClosest = self.getClosest(end)
            self.adjList[end] = {}
            self.adjList[end][endClosest] = getEuclideanDist(end,endClosest)
            self.adjList[endClosest][end] = getEuclideanDist(endClosest,end)
        return self.adjList.copy()

################################################################################
### PathFunctions
################################################################################

### A* #########################################################################
def getAStar(navMap, start, end):
    adjList = navMap.getAdjList(start,end)

    g       = {start:0}
    parent  = {start:start}
    opened  = {start:g[start]}
    closed  = {}

    while len(opened) > 0:
        s = min(opened.keys(), key=lambda x:opened[x])
        del opened[s]

        if s == end:
            path = []
            while s != start:
                path.append(s)
                s = parent[s]
            path.append(start)
            path.reverse()
            return path

        closed[s] = True

        for s_ in adjList[s]:
            if not (s_ in closed):
                if not (s_ in opened):
                    g[s_] = INFINITY
                    parent[s_] = None
                UpdateVertex(s, s_, g, opened, parent, end)
    return []


def UpdateVertex(s, s_, g, opened, parent, end):
    c = getEuclideanDist(s,s_)
    if ((g[s] + c) < g[s_]):
        g[s_] = g[s] + c
        parent[s_] = s
        if (s_ in opened):
            del opened[s_]
        opened[s_] = g[s_] + getEuclideanDist(s_,end)


### A* Post-Smoothing ##########################################################
def getAStarPS(navMap, worldMap, start_, end_):
    s = getAStar(navMap,start_,end_)

    if(len(s)):
        k = 0
        t = {k:s[0]}
        for i in range(1,len(s)-1):
            if not worldMap.lineOfSight(t[k],s[i+1]):
                k += 1
                t[k] = s[i]
        k += 1
        t[k] = s[len(s)-1]

        path = [v for v in t.values()]
        return path
    else:
        return s


### Theta* #####################################################################
def getThetaStar(navMap, worldMap, start, end):
    adjList = navMap.getAdjList(start,end)

    g       = {start:0}
    parent  = {start:start}
    opened  = {start:g[start]}
    closed  = {}

    while len(opened) > 0:
        s = min(opened.keys(), key=lambda x:opened[x])
        del opened[s]

        if s == end:
            path = []
            while s != start:
                path.append(s)
                s = parent[s]
            path.append(start)
            path.reverse()
            return path

        closed[s] = True

        for s_ in adjList[s]:
            if not (s_ in closed):
                if not (s_ in opened):
                    g[s_] = INFINITY
                    parent[s_] = None
                UpdateVertexTheta(s, s_, g, opened, parent, end, worldMap)
    return []

def UpdateVertexTheta(s, s_, g, opened, parent, end, worldMap):
    if (worldMap.lineOfSight(parent[s],s_)):
        c = getEuclideanDist(parent[s],s_)
        if g[parent[s]] + c < g[s_]:
            g[s_] = g[parent[s]] + c
            parent[s_] = parent[s]
            if (s_ in opened):
                del opened[s_]
            opened[s_] = g[s_] + getEuclideanDist(s_,end)
    else:
        c = getEuclideanDist(s,s_)
        if ((g[s] + c) < g[s_]):
            g[s_] = g[s] + c
            parent[s_] = s
            if (s_ in opened):
                del opened[s_]
            opened[s_] = g[s_] + getEuclideanDist(s_,end)        

### RDP ########################################################################
def getRDP(navMap, worldMap, start_, end_):
    path = getAStar(navMap, start_, end_)
    if(len(path) < 1):
        return path

    path = RDPsub(path, worldMap)

    return path

def RDPsub(path,worldMap):
    firstPoint  = path[0]
    lastPoint   = path[-1]
    if (len(path)<3):
        return path

    index = -1
    dist = 0
    for i in range(len(path)):
        cDist = findPerpendicularDistance(path[i],firstPoint,lastPoint)
        if (cDist > dist):
            dist = cDist
            index = i
    if (dist > RDP_EPSILON):
        l1 = path[0:index+1]
        l2 = path[index:]
        r1 = RDPsub(l1,worldMap)
        r2 = RDPsub(l2,worldMap)
        rs = r1
        rs.extend(r2)
        return rs
    elif(worldMap.lineOfSight(firstPoint,lastPoint)):
        return [firstPoint,lastPoint]
    else:
        return path
        

def findPerpendicularDistance(p, p1, p2):
    if(p1[0] == p2[0]):
        result = abs(p[0]-p1[0])
    else:
        slope = (p2[1] - p1[1]) / (p2[0] - p1[0])
        intercept = p1[1] - (slope * p1[0])
        result = abs(slope * p[0] - p[1] + intercept) / sqrt(pow(slope,2) + 1)

    return result

### RPF ########################################################################
def getRPF(navMap, worldMap, start_, end_):
    path = getAStar(navMap, start_, end_)
    if(len(path) < 1):
        return path
    rpfPath = [path[0]]
    currP   = path[0]
    while(not(currP == path[-1])):
        for i in reversed(range(len(path))):
            if(i == 1):
                #Sanity check - if the only point left is the next one on normal
                #   A-star path, use it!
                currP = path[1]
                rpfPath.append(currP)
                path = path[1:]
                break
            dist = getEuclideanDist(currP,path[i])
            if((dist<=RPF_MAX_DIST) and (worldMap.lineOfSight(currP,path[i]))):
                currP = path[i]
                rpfPath.append(currP)
                path = path[i:]
                break
    return rpfPath


### Distance Check #############################################################
def getFullCardinalPath(worldMap, path):
    cardinalpath = []
    if(len(path)>1):
        #print(path)
        for i in range(len(path)-1):
            smallpath = worldMap.getCardinalPath(path[i],path[i+1])
            cardinalpath.extend(smallpath)
        cardinalpath.append(path[-1])
        #print(cardinalpath)
    return cardinalpath

def getDistance(worldMap, path):
    sqrt2 = sqrt(2)
    sqrt2count = 0
    count = 0
    cardinalpath = getFullCardinalPath(worldMap, path)
    for i in range(len(cardinalpath)-1):
        #print(cardinalpath[i])
        x0, y0 = cardinalpath[i]
        x1, y1 = cardinalpath[i+1]

        if(abs(x0-x1)>1 or abs(y0-y1)>1):
            print(x0, y0, x1, y1)
            print("Big diff!")
 
        if((x0 == x1) or (y0 == y1)):
            count += 1
        else:
            if(worldMap.checkCell((x0,y1))):
                #print(x0, y0, x1, y1)
                #print("Diagonal cross (x0, y1): " + str((x0,y1)))
                count += 2
            elif(worldMap.checkCell((x1,y0))):
                #print(x0, y0, x1, y1)
                #print("Diagonal cross (x1, y0): " + str((x1,y0)))
                count += 2
            else:
                sqrt2count += 1

    return (round(count + sqrt2count*sqrt2,2))















