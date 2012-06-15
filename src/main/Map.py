from pandac.PandaModules import *
from panda3d.bullet import BulletPlaneShape
from panda3d.bullet import BulletRigidBodyNode
from panda3d.bullet import BulletTriangleMesh
from panda3d.bullet import BulletTriangleMeshShape

from panda3d.core import GeomVertexData
from panda3d.core import GeomVertexReader
from panda3d.core import InternalName

from math import floor
from pathfind.Region import *
from pathfind.Portal import *

import sys

class Map(object):
    
    def __init__(self, mainReference):
        self.mainRef = mainReference
        
        # fog experiment
        myFog = Fog("Mist")
        myFog.setColor(0.6, 0.6, 0.6)
        myFog.setExpDensity(0.0007)
        render.setFog(myFog)
        


        # loading H_Block
        self.H_Block = loader.loadModel("../../models/H_Block/H_Block")
        self.H_Block.reparentTo(self.mainRef.render)
        
        # loading H_Block's colision mesh
        self.H_Block_col = loader.loadModel("../../models/H_Block/H_Block_colision")
        
        # creating triangle meshes for all static nodes
        self.hBlockRoomGeom = self.H_Block_col.getChild(0).getNode(0).getGeom(0)
        self.hBlockBulletMesh = BulletTriangleMesh()
        self.hBlockBulletMesh.addGeom(self.hBlockRoomGeom)
        self.hBlockBulletShape = BulletTriangleMeshShape(self.hBlockBulletMesh, dynamic=False)
        self.bulletHBlockNode = BulletRigidBodyNode('hBlockNode')
        self.bulletHBlockNode.addShape(self.hBlockBulletShape)
        self.mainRef.world.attachRigidBody(self.bulletHBlockNode)
        
        
        self.pathRegions = []
        
        self.pathGeometry = loader.loadModel("../../models/H_Block/path")
        
        for convexRegion in self.pathGeometry.getChild(0).getChildren():
            regionNode = convexRegion.getNode(0)
            regionsStr = regionNode.getTag("t") # syntax: myRegion, regionsConnectedToMe[?]
            regionsArray = regionsStr.split(",")
            self.pathRegions.append( Region(regionsArray[0], regionsArray[1:]) ) 
            #self.pathRegions[-1].vertices = regionNode.getGeom(0).getVertexData()
            #print self.pathRegions[-1].vertices

            # Copy vertices
            vertexReader = GeomVertexReader(regionNode.getGeom(0).getVertexData(), InternalName.getVertex())
            while( not(vertexReader.isAtEnd() ) ):
                data = vertexReader.getData3()
                X = data.getX()
                Y = data.getY()
                Z = data.getZ()
                self.pathRegions[-1].vertices.append((X,Y,Z))
                
        print self.pathRegions[-1].vertices

######### for path finding
        # collect points
#        self.pathGeomNodes  = self.H_Block.find('**/static_nodes/floor')
#        self.pathGeomNode   = self.pathGeomNodes.node()
#        self.pathVertexData = self.pathGeomNode.getGeom(0).getVertexData()
#        # read only vertices
#        vertexReader = GeomVertexReader(self.pathVertexData, InternalName.getVertex())
#        self.pathPoints = [None]*64 # hardcoded
#        
#        # Minheap test
#        minHeapX = MinHeap(64,True,"X") # hardcoded
#        minHeapY = MinHeap(64,True,"Y") # hardcoded
#        minHeapZ = MinHeap(64,True,"Z") # hardcoded
#        
#        pointsCount = 0
#        while( not(vertexReader.isAtEnd() ) ):
#            i = vertexReader.getData3()
#            # we are converting to int to avoid repeated vertices
#            X = int(i.getX())
#            Y = int(i.getY())
#            Z = int(i.getZ())
#            tmp = PathPoint(X,Y,Z,pointsCount) # pointsCount for arrayID
#            self.pathPoints[pointsCount] = tmp
#            minHeapX.Add(tmp)
#            minHeapY.Add(tmp)
#            minHeapZ.Add(tmp)
#            pointsCount+=1
#        
#        xGridIndex  = 0
#        self.xPosInterval = sys.float_info.max
#        xPastPP = None
#        while(minHeapX.count > 0):
#            xPP = minHeapX.ExtractFirst()
#            if (type(xPastPP) == PathPoint):
#                if (self.pathPoints[xPastPP.arrayID].X != self.pathPoints[xPP.arrayID].X):
#                    xGridIndex+=1
#                    if (self.xPosInterval == sys.float_info.max):
#                        self.xPosInterval = xPP.X - xPastPP.X
#                    else:
#                        if( 1 < abs(self.xPosInterval - (xPP.X - xPastPP.X) ) ):
#                            # irregular interval on X Axis
#                            raise Exception()
#            xPP.gridPosX = xGridIndex
#            xPastPP = xPP
#            
#        yGridIndex = 0
#        self.yPosInterval = sys.float_info.max
#        yPastPP = None
#        while(minHeapY.count > 0):
#            yPP = minHeapY.ExtractFirst()
#            if (type(yPastPP) == PathPoint):
#                if (self.pathPoints[yPastPP.arrayID].Y != self.pathPoints[yPP.arrayID].Y):
#                    yGridIndex+=1
#                    if (self.yPosInterval == sys.float_info.max):
#                        self.yPosInterval = yPP.Y - yPastPP.Y
#                    else:
#                        if( 1 < abs(self.yPosInterval - (yPP.Y - yPastPP.Y) ) ):
#                            # irregular interval on Y Axis
#                            raise Exception()
#            yPP.gridPosY = yGridIndex
#            yPastPP = yPP
#            
#        zGridIndex = 0
#        self.zPosInterval = sys.float_info.max
#        zPastPP = None
#        while(minHeapZ.count > 0):
#            zPP = minHeapZ.ExtractFirst()
#            if (type(zPastPP) == PathPoint):
#                if (self.pathPoints[zPastPP.arrayID].Z != self.pathPoints[zPP.arrayID].Z):
#                    zGridIndex+=1
#                    if (self.zPosInterval == sys.float_info.max):
#                        self.zPosInterval = zPP.Z - zPastPP.Z
#                    else:
#                        if( 1 < abs(self.zPosInterval - (zPP.Z - zPastPP.Z) ) ):
#                            # irregular interval on Z Axis
#                            raise Exception()
#            zPP.gridPosZ = zGridIndex
#            zPastPP = zPP
#         
#        # debug purposes   
##        for i in range(len(self.pathPoints)):
##            print "gridX: " + str(self.pathPoints[i].gridPosX) + " gridY: " + str(self.pathPoints[i].gridPosY) + " gridZ: " + str(self.pathPoints[i].gridPosZ)
##            print "posX: " + str(self.pathPoints[i].X) + " posY: " + str(self.pathPoints[i].Y) + " posZ: " + str(self.pathPoints[i].Z)
#            
#        # creating path world
#        self.AIworld = PathWorld(xGridIndex+1,yGridIndex+1,zGridIndex+1)
#        # adding allowed vertices
#        for i in range(len(self.pathPoints)):
#            point = self.pathPoints[i]
#            self.AIworld.MarkPosition(point, False)
#########
