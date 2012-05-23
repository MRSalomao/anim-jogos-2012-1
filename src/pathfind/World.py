"""
    @author: Roy Triesscheijn (http://www.royalexander.wordpress.com)
    @change by Guilherme Silva Senges
        - Adapted to Panda3D engine on Python language
    Sample World class that only provides 'is free or not' information on a node
"""

from Point3D import *
from PathPoint import *

class World(object):
            
    # Note: we use Z as height and Y as depth here!
    def Left(self):
        return 0
    def Right(self):
        return len(self.worldBlocked)
    def Bottom(self): 
        return 0
    def Top(self):
        return len(self.worldBlocked[0][0])
    def Front(self):
        return 0
    def Back(self):
        return len(self.worldBlocked[0])

    ## Creates a 3D world
    # for a 2D world assign depth value to 1
    def __init__(self, width, depth, height):  
        self.worldBlocked = [ [ [True]*height ]*depth ]*width  # extremely simple world where each node can be free or blocked: true=blocked

    ## Mark positions in the world as blocked (true) or unblocked (false)
    # parameter value: use true if you wan't to block the value
    def MarkPosition(self, point, boolValue):
        if (type(point) == PathPoint):
            self.worldBlocked[ point.gridPosX][ point.gridPosY][ point.gridPosZ ] = boolValue
        else:
            raise Exception()

    ## Checks if a position is free or marked (and legal)        
    # return true if the position is free
    def PositionIsFree(self, point):
        if (type(point) == PathPoint):
            conditionX = (point.gridPosX >= 0) and (point.gridPosX < len(self.worldBlocked))
            conditionY = (point.gridPosY >= 0) and (point.gridPosY < len(self.worldBlocked[0]))
            conditionZ = (point.gridPosZ >= 0) and (point.gridPosZ < len(self.worldBlocked[0][0]))
            isFree = (not(self.worldBlocked[point.gridPosX][point.gridPosY][ point.gridPosZ]))
            return conditionX and conditionY and conditionZ and isFree
        else:
            raise Exception()            
