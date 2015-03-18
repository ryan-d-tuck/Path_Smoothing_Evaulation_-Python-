import pygame, sys, os

from constants import *


################################################################################
### Drawer
################################################################################
class Drawer:
    def __init__(self, screen):
        self.screen     = screen

    def DrawWorldMap(self, worldMap):
        width   = worldMap.width
        height  = worldMap.height
        
        for x in range(width):
            for y in range(height):
                if worldMap.checkCell((x,y)):
                    self.screen.set_at((int(x),int(y)), WORLD_BLOCK_COLOR)

    def DrawQuadTree(self, quadTree, leafOnly = True):
        drawNode = True
        if(leafOnly):
            if (quadTree.nodes):
                drawNode = False

        if(drawNode):
            if(quadTree.fill == QT_EMPTY):
                pygame.draw.rect(self.screen, QUAD_EMPTY_LINE_COLOR, quadTree.getRect(), 1)
            elif(quadTree.fill == QT_FULL):
                pygame.draw.rect(self.screen, QUAD_FULL_LINE_COLOR, quadTree.getRect(), 1)
            else:
                pygame.draw.rect(self.screen, QUAD_OPEN_LINE_COLOR, quadTree.getRect(), 1)
            

        if(quadTree.nodes):
            for loc in ["UL","UR","LL","LR"]:
                if(loc in quadTree.nodes):
                    self.DrawQuadTree(quadTree.nodes[loc], leafOnly)

    def DrawNavMap(self, navMap):
        for point in navMap.adjList.keys():
            for adjPoint in navMap.adjList[point].keys():
                pygame.draw.line(self.screen, NAV_LINE_COLOR, point, adjPoint)

        for point in navMap.adjList.keys():
            self.screen.set_at((int(point[0]),int(point[1])), NAV_NODE_COLOR)

    def DrawPath(self, path):
        for i in range(len(path)-1):
            pygame.draw.line(self.screen, PATH_LINE_COLOR, path[i], path[i+1], 2)
            
