import pygame, sys, os
from math import ceil,floor,sqrt
from collections import defaultdict

from pygame.locals import *

#import pygbutton
import pathfinding as pf
import drawer as dw
import helperfunctions as hf
from constants import *

################################################################################
### Pygame intialization
################################################################################

#Pygame Inits
pygame.init()
screen = pygame.display.set_mode(
            (SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

pygame.display.set_caption("Map Viewer")
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
    start = fpsClock.tick()
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

    end = fpsClock.tick()

    time_average = end / TIMES_TO_RUN_ALG
    dist = pf.getDistance(mapGrid,path)
    printPathInfo(time_average,dist)
    return path

def printScenInfo(current):
    print("")
    print("### Scenario " + str(current["num"]) + " Info ####")
    print("Str: ", str(current["x0"])+ ", " +str(current["y0"]))
    print("End: ", str(current["x1"])+ ", " +str(current["y1"]))
    print("Opt: ", current["opt"])

def printPathInfo(time,dist):
    print("### Path Info ####")
    print("Time: ", str(time) + "ms")
    print("Dist: ", str(dist))

################################################################################
### Start of Main
################################################################################

### Game Loop Inits ############################################################
mapGrid     = pf.WorldMap(getMapPath())
scen        = pf.ScenInfo(getScenPath())
drawer      = dw.Drawer(screen)
quad        = pf.QuadTreeNode(0,0,mapGrid.width,mapGrid.height)
quad.check(mapGrid)
flatQuad    = quad.getFlattened()
navMap      = pf.NavMap(flatQuad)


scen.loadNum(3)
current = scen.getCurr()
p0 = (current["x0"],current["y0"])
p1 = (current["x1"],current["y1"])
printScenInfo(current)
path = runAlgorithm(navMap,mapGrid,p0,p1)


### Main Game Loop #############################################################
while True:
    delta = fpsClock.tick(50)
    screen.fill(BG_COLOR)

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == MOUSEBUTTONDOWN:
            if event.button == LEFT:
                current = scen.getNext()
                p0 = (current["x0"],current["y0"])
                p1 = (current["x1"],current["y1"])
                printScenInfo(current)
                path = runAlgorithm(navMap,mapGrid,p0,p1)
            elif event.button == RIGHT:
                current = scen.getPrev()
                p0 = (current["x0"],current["y0"])
                p1 = (current["x1"],current["y1"])
                printScenInfo(current)
                path = runAlgorithm(navMap,mapGrid,p0,p1)

        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.event.post(pygame.event.Event(QUIT))

    #Update

    #Draw
    drawer.DrawWorldMap(mapGrid)
    #drawer.DrawQuadTree(quad)
    for rect in flatQuad:
        pygame.draw.rect(screen, QUAD_EMPTY_LINE_COLOR, rect, 1)
    #drawer.DrawNavMap(navMap)
    drawer.DrawPath(path)

    #Flip display
    pygame.display.flip()

