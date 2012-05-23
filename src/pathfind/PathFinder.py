"""
    @author: Roy Triesscheijn (http://www.royalexander.wordpress.com)
    @change by Guilherme Silva Senges
        - Adapted to Panda3D engine on Python language
    Class providing 3D pathfinding capabilities using A*.
    Heaviliy optimized for speed therefore uses slightly more memory
    On rare cases finds the 'almost optimal' path instead of the perfect path
    this is because we immediately return when we find the exit instead of finishing
    'neighbour' loop.
"""
from MinHeap import *
from BreadCrumb import *
from PathPoint import *

class Path_Finder(object):
    
    ## Method that switfly finds the best path from start to end.
    # Returns the starting breadcrumb traversable via .next to the end or null if there is no path        
    def __init__(self, world, start, end, preCrumbsList, xInterval, yInterval, zInterval):
        
        # Neighbour options
        self.surrounding = [                        
            # Top slice (Y=1)
            PathPoint(-xInterval,yInterval,zInterval,None,-1,1,1), PathPoint(0,yInterval,zInterval,None,0,1,1), PathPoint(xInterval,yInterval,zInterval,None,1,1,1),
            PathPoint(-xInterval,yInterval,0,None,-1,1,0), PathPoint(0,yInterval,0,None,0,1,0), PathPoint(xInterval,yInterval,0,None,1,1,0),
            PathPoint(-xInterval,yInterval,-zInterval,None,-1,1,-1), PathPoint(0,yInterval,-zInterval,None,0,1,-1), PathPoint(xInterval,yInterval,-zInterval,None,1,1,-1),
            # Middle slice (Y=0)
            PathPoint(-xInterval,0,zInterval,None,-1,0,1), PathPoint(0,0,zInterval,None,0,0,1), PathPoint(xInterval,0,zInterval,None,1,0,1),
            PathPoint(-xInterval,0,0,None,-1,0,0), PathPoint(xInterval,0,0,None,1,0,0), # (0,0,0) is self
            PathPoint(-xInterval,0,-zInterval,None,-1,0,-1), PathPoint(0,0,-zInterval,None,0,0,-1), PathPoint(xInterval,0,-zInterval,None,1,0,-1),
            # Bottom slice (Y=-1)
            PathPoint(-xInterval,-yInterval,zInterval,None,-1,-1,1), PathPoint(0,-yInterval,zInterval,None,0,-1,1), PathPoint(xInterval,-yInterval,zInterval,None,1,-1,1),
            PathPoint(-xInterval,-yInterval,0,None,-1,-1,0), PathPoint(0,-yInterval,0,None,0,-1,0), PathPoint(xInterval,-yInterval,0,None,1,-1,0),
            PathPoint(-xInterval,-yInterval,-zInterval,None,-1,-1,-1), PathPoint(0,-yInterval,-zInterval,None,0,-1,-1), PathPoint(xInterval,-yInterval,-zInterval,None,1,-1,-1)            
        ]
        
        # note we just flip start and end here so you don't have to.            
        return self.FindPathReversed(world, end, start, preCrumbsList) 

    ## Method that switfly finds the best path from start to end. Doesn't reverse outcome
    # Returns the end breadcrump where each .next is a step back)
    def FindPathReversed(self, world, start, end, preCrumbsList):
        self.openList = MinHeap(256)
        
        self.brWorld = [ [ [ None for i in range(world.Back() ) ] for j in range(world.Top() ) ] for k in range(world.Right() )]
        
        # initializing crumbs
        for i in range(len(preCrumbsList)):
            point = preCrumbsList[i]
            self.brWorld[point.gridPosX][point.gridPosY][point.gridPosZ] = BreadCrumb(point)
            
        # BreadCrumb
        self.node = None
        # point3D
        self.tmp = None
        
        self.cost = None
        self.diff = 0
     
        self.current = BreadCrumb(start)
        self.current.cost = 0

        self.finish = BreadCrumb(end)
        self.brWorld[self.current.point.gridPosX][self.current.point.gridPosY][self.current.point.gridPosZ] = self.current
        self.openList.Add(self.current)

        while (self.openList.getCount() > 0):
            # Find best item and switch it to the 'closedList'
            self.current = self.openList.ExtractFirst()                                              
            self.current.onClosedList = True                

            # Find neighbours
            for i in range(len(self.surrounding)):
                self.tmp = self.current.point + self.surrounding[i]
                
                if ( (self.tmp.gridPosX <= (world.Right() -1)) and (self.tmp.gridPosY <= (world.Top() -1)) and (self.tmp.gridPosZ <= (world.Back() -1)) ):
                    if (world.PositionIsFree(self.tmp)):
                        # Check if we've already examined a neighbour, if not create a new node for it.
                        if (self.brWorld[self.tmp.gridPosX][ self.tmp.gridPosY][ self.tmp.gridPosZ] == None):
                            self.node = BreadCrumb(self.tmp)
                            self.brWorld[self.tmp.gridPosX][ self.tmp.gridPosY][ self.tmp.gridPosZ] = self.node
                        else:
                            self.node = self.brWorld[self.tmp.gridPosX][ self.tmp.gridPosY][ self.tmp.gridPosZ]
    
                        # If the node is not on the 'closedList' check it's new score, keep the best
                        if (not(self.node.onClosedList)):                            
                            self.diff = 0
                            if (self.current.point.X != self.node.point.X):
                                self.diff += 1
                            if (self.current.point.Y != self.node.point.Y):
                                self.diff += 1
                            if (self.current.point.Z != self.node.point.Z):
                                self.diff += 1
                            self.cost = self.current.cost + self.diff + self.node.point.getDistanceSquared(end)
                            
                            if (self.cost < self.node.cost):  
                                self.node.cost = self.cost
                                self.node.next = self.current
                            # If the node wasn't on the selfopenList yet, add it 
                            if (not(self.node.onOpenList)):                         
                                # Check to see if we're done
                                if (self.node == self.finish):
                                    self.node.next = self.current
                                    return None # success
                                self.node.onOpenList = True
                                self.openList.Add(self.node)  
                                                  
        return None # no path found                                    
