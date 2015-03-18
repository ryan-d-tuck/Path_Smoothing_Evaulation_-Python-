import pygame, sys, os
from math import ceil,floor,sqrt
from collections import defaultdict

from pygame.locals import *

import pathfinding as pf
import drawer as dw
import helperfunctions as hf
from constants import *

################################################################################
### Pygame intialization
################################################################################

pygame.init()
fpsClock = pygame.time.Clock()

################################################################################
### Helper Functions
################################################################################
""" A few functions to make it more clear what exactly is happening by creating
    cleaner looking code.
"""
def getMapPath():
    return os.path.join(SYS_PATH,"map",MAP_NAME+".map")

def getScenPath():
    return os.path.join(SYS_PATH,"map",MAP_NAME+".map.scen")

def runAlgorithm(navMap,mapGrid,p0,p1):
    for i in range(TIMES_TO_RUN_ALG):
        if(CURR_ALG == ALG_ASTAR):
            path = pf.getAStar(navMap,p0,p1)

        elif(CURR_ALG == ALG_ASTAR_PS):
            path = pf.getAStarPS(navMap,mapGrid,p0,p1)

        elif(CURR_ALG == ALG_THETA_STAR):
            path = pf.getThetaStar(navMap,mapGrid,p0,p1)

        elif(CURR_ALG == ALG_RDP):
            path = pf.getRDP(navMap,mapGrid,p0,p1)

        elif(CURR_ALG == ALG_RPF):
            path = pf.getRPF(navMap,mapGrid,p0,p1)
    return path

def printFileName():
    ret_str = MAP_NAME + '_'
    if(CURR_ALG == ALG_ASTAR):
        ret_str += 'A_star'
    elif(CURR_ALG == ALG_ASTAR_PS):
        ret_str += 'A_star_ps'
    elif(CURR_ALG == ALG_THETA_STAR):
        ret_str += 'Theta_star'
    elif(CURR_ALG == ALG_RDP):
        ret_str += 'RDP'
    elif(CURR_ALG == ALG_RPF):
        ret_str += 'RPF'
    ret_str += '.csv'
    return ret_str

def printCategories():
    ret_str = "Bucket,start-x,start-y,goal-x,goal-y,dist,time(ms),optimal\n"
    return ret_str


################################################################################
### Start of Main
################################################################################

### Game Loop Inits ############################################################
mapGrid     = pf.WorldMap(getMapPath())
scen        = pf.ScenInfo(getScenPath())
#drawer      = dw.Drawer(screen)
quad        = pf.QuadTreeNode(0,0,mapGrid.width,mapGrid.height)
quad.check(mapGrid)
flatQuad    = quad.getFlattened()
navMap      = pf.NavMap(flatQuad)


f           = open(printFileName(), 'w')
f.write(printCategories())

current = scen.getCurr()
p0 = (current["x0"],current["y0"])
p1 = (current["x1"],current["y1"])

start = fpsClock.tick()
path = runAlgorithm(navMap,mapGrid,p0,p1)
end = fpsClock.tick()

time_average = end / TIMES_TO_RUN_ALG
dist = pf.getDistance(mapGrid,path)

print_str = (str(current["num"]) + ',' + 
    str(current["x0"])+ ',' + str(current["y0"]) + ',' +
    str(current["x1"])+ ',' +str(current["y1"]) + ',' +
    str(dist) + ',' + str(time_average) + ',' + str(current["opt"]) + "\n")
f.write(print_str)

### Main Game Loop #############################################################
while True:
    numOld = scen.getCurrInd()
    current = scen.getNext()
    num = scen.getCurrInd()
    p0 = (current["x0"],current["y0"])
    p1 = (current["x1"],current["y1"])

    start = fpsClock.tick()
    path = runAlgorithm(navMap,mapGrid,p0,p1)
    end = fpsClock.tick()

    time_average = end / TIMES_TO_RUN_ALG
    dist = pf.getDistance(mapGrid,path)

    print_str = (str(current["num"]) + ',' + 
        str(current["x0"])+ ',' + str(current["y0"]) + ',' +
        str(current["x1"])+ ',' +str(current["y1"]) + ',' +
        str(dist) + ',' + str(time_average) + ',' + str(current["opt"]) + "\n")
    f.write(print_str)
    print("Number: ", num)    

    if numOld > num:
        pygame.quit()
        sys.exit()
