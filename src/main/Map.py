from pandac.PandaModules import *
from panda3d.bullet import BulletPlaneShape
from panda3d.bullet import BulletRigidBodyNode
from panda3d.bullet import BulletTriangleMesh
from panda3d.bullet import BulletTriangleMeshShape

from panda3d.core import GeomVertexData
from panda3d.core import GeomVertexReader
from panda3d.core import InternalName

from math import floor
from pathfind import *
from pathfind.PathPoint import *

import sys

class Map(object):
    
    def __init__(self, mainReference):
        self.mainRef = mainReference
        
        # fog experiment
        myFog = Fog("Mist")
        myFog.setColor(0.6, 0.6, 0.6)
        myFog.setExpDensity(0.0007)
        render.setFog(myFog)

        # loading h_208 room
        self.h208Room = loader.loadModel("../../models/model_h208/h_208")
        self.h208Room.reparentTo(self.mainRef.render)
        
        # creating triangle meshes for all static nodes
        self.staticH208Nodes = self.h208Room.find('**/static_nodes')
        self.h208RoomNodes = self.staticH208Nodes.findAllMatches('**/+GeomNode')
        for i in range( self.h208RoomNodes.getNumPaths()):
            self.h208RoomGeomNode = self.h208RoomNodes.getPath(i).node()
            self.h208RoomGeom = self.h208RoomGeomNode.getGeom(0)
            self.h208RoomBulletMesh = BulletTriangleMesh()
            self.h208RoomBulletMesh.addGeom(self.h208RoomGeom)
            self.h208RoomBulletShape = BulletTriangleMeshShape(self.h208RoomBulletMesh, dynamic=False)
            self.bulletH208RoomNode = BulletRigidBodyNode('h_208_node'+str(i))
            self.bulletH208RoomNode.addShape(self.h208RoomBulletShape)
            self.mainRef.world.attachRigidBody(self.bulletH208RoomNode)
            
######### for path finding
        # collect points
        self.pathGeomNodes  = self.h208Room.find('**/static_nodes/floor')
        self.pathGeomNode   = self.pathGeomNodes.node()
        self.pathVertexData = self.pathGeomNode.getGeom(0).getVertexData()
        # read only vertices
        vertexReader = GeomVertexReader(self.pathVertexData, InternalName.getVertex())
        self.pathPoints = [None]*64 # hardcoded
        
        # Minheap test
        minHeapX = MinHeap(64,True,"X") # hardcoded
        minHeapY = MinHeap(64,True,"Y") # hardcoded
        minHeapZ = MinHeap(64,True,"Z") # hardcoded
        
        pointsCount = 0
        while( not(vertexReader.isAtEnd() ) ):
            i = vertexReader.getData3()
            # we are converting to int to avoid repeated vertices
            X = int(i.getX())
            Y = int(i.getY())
            Z = int(i.getZ())
            tmp = PathPoint(X,Y,Z,pointsCount) # pointsCount for arrayID
            self.pathPoints[pointsCount] = tmp
            minHeapX.Add(tmp)
            minHeapY.Add(tmp)
            minHeapZ.Add(tmp)
            pointsCount+=1
        
        xGridIndex  = 0
        self.xPosInterval = sys.float_info.max
        xPastPP = None
        while(minHeapX.count > 0):
            xPP = minHeapX.ExtractFirst()
            if (type(xPastPP) == PathPoint):
                if (self.pathPoints[xPastPP.arrayID].X != self.pathPoints[xPP.arrayID].X):
                    xGridIndex+=1
                    if (self.xPosInterval == sys.float_info.max):
                        self.xPosInterval = xPP.X - xPastPP.X
                    else:
                        if( 1 < abs(self.xPosInterval - (xPP.X - xPastPP.X) ) ):
                            # irregular interval on X Axis
                            raise Exception()
            xPP.gridPosX = xGridIndex
            xPastPP = xPP
            
        yGridIndex = 0
        self.yPosInterval = sys.float_info.max
        yPastPP = None
        while(minHeapY.count > 0):
            yPP = minHeapY.ExtractFirst()
            if (type(yPastPP) == PathPoint):
                if (self.pathPoints[yPastPP.arrayID].Y != self.pathPoints[yPP.arrayID].Y):
                    yGridIndex+=1
                    if (self.yPosInterval == sys.float_info.max):
                        self.yPosInterval = yPP.Y - yPastPP.Y
                    else:
                        if( 1 < abs(self.yPosInterval - (yPP.Y - yPastPP.Y) ) ):
                            # irregular interval on Y Axis
                            raise Exception()
            yPP.gridPosY = yGridIndex
            yPastPP = yPP
            
        zGridIndex = 0
        self.zPosInterval = sys.float_info.max
        zPastPP = None
        while(minHeapZ.count > 0):
            zPP = minHeapZ.ExtractFirst()
            if (type(zPastPP) == PathPoint):
                if (self.pathPoints[zPastPP.arrayID].Z != self.pathPoints[zPP.arrayID].Z):
                    zGridIndex+=1
                    if (self.zPosInterval == sys.float_info.max):
                        self.zPosInterval = zPP.Z - zPastPP.Z
                    else:
                        if( 1 < abs(self.zPosInterval - (zPP.Z - zPastPP.Z) ) ):
                            # irregular interval on Z Axis
                            raise Exception()
            zPP.gridPosZ = zGridIndex
            zPastPP = zPP
         
        # debug purposes   
#        for i in range(len(self.pathPoints)):
#            print "gridX: " + str(self.pathPoints[i].gridPosX) + " gridY: " + str(self.pathPoints[i].gridPosY) + " gridZ: " + str(self.pathPoints[i].gridPosZ)
#            print "posX: " + str(self.pathPoints[i].X) + " posY: " + str(self.pathPoints[i].Y) + " posZ: " + str(self.pathPoints[i].Z)
            
        # creating path world
        self.AIworld = PathWorld(xGridIndex+1,yGridIndex+1,zGridIndex+1)
        # adding allowed vertices
        for i in range(len(self.pathPoints)):
            point = self.pathPoints[i]
            self.AIworld.MarkPosition(point, False)
#########


        # loading test room
        self.testRoom = loader.loadModel("../../models/sala_teste")
        self.testRoom.reparentTo(self.mainRef.render)
        self.testRoom.setPos(500, 0, -35)
        self.testRoom.setScale(34, 34, 34)
        
        self.lightMapTS = TextureStage('LightMap')
        self.lightMapTS.setMode(TextureStage.MModulate)
        self.lightMapTS.setTexcoordName("ul")     
        
        levelGeomNodes = self.testRoom.getChild(0).getChildren()
        
        for levelGeomNode in levelGeomNodes:
        
            self.lightMapTexture = loader.loadTexture("../../models/" + levelGeomNode.getName() + ".png")  
            levelGeomNode.setTexture(self.lightMapTS, self.lightMapTexture)
        
