from pandac.PandaModules import *
from panda3d.bullet import BulletPlaneShape
from panda3d.bullet import BulletRigidBodyNode
from panda3d.bullet import BulletTriangleMesh
from panda3d.bullet import BulletTriangleMeshShape

from panda3d.core import GeomVertexData
from panda3d.core import GeomVertexReader
from panda3d.core import InternalName
from panda3d.core import Vec3

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
        self.H_Block_col = loader.loadModel("../../models/H_Block/H_Block_collision")
        
        # creating triangle meshes for all static nodes
        self.hBlockRoomGeom = self.H_Block_col.getChild(0).getNode(0).getGeom(0)
        self.hBlockBulletMesh = BulletTriangleMesh()
        self.hBlockBulletMesh.addGeom(self.hBlockRoomGeom)
        self.hBlockBulletShape = BulletTriangleMeshShape(self.hBlockBulletMesh, dynamic=False)
        self.bulletHBlockNode = BulletRigidBodyNode('hBlockNode')
        self.bulletHBlockNode.addShape(self.hBlockBulletShape)
        self.mainRef.world.attachRigidBody(self.bulletHBlockNode)
        
        # arrays containing all regions and portals dividing those regions
        self.convexRegions = []
        self.portals = []
        
        self.convexRegionsGeometry = loader.loadModel("../../models/H_Block/ConvexRegions2")
        self.portalsGeometry = loader.loadModel("../../models/H_Block/Portals2")
        self.portalsGeometry.reparentTo(self.mainRef.render)
        
        # Regions
        for convexRegion in self.convexRegionsGeometry.getChild(0).getChildren():
            regionNode = convexRegion.getNode(0)
            regionID = regionNode.getTag("prop")
            self.convexRegions.append( Region(regionID) )

            # Get vertices that define the convex region
            vertexReader = GeomVertexReader(regionNode.getGeom(0).getVertexData(), InternalName.getVertex())
            while( not(vertexReader.isAtEnd() ) ):
                data = vertexReader.getData3()
                X = data.getX()
                Y = data.getY()
                Z = data.getZ()
                self.convexRegions[-1].vertices.append((X,Y,Z))
                
        self.convexRegions = sorted(self.convexRegions, key=lambda convexRegion: convexRegion.regionID)
        # Debug
#        for cr in self.convexRegions: 
#            print cr.regionID

        # Portals
        for portal in self.portalsGeometry.getChild(0).getChildren():
            portalNode = portal.getNode(0)

            # Get vertices that define the portal
            frontiers = []
            vertexReader = GeomVertexReader(portalNode.getGeom(0).getVertexData(), InternalName.getVertex())
            for i in range(2):  # We got 2 vertices per portal
                data = vertexReader.getData3()
                X = data.getX()
                Y = data.getY()
                Z = data.getZ()
                frontiers.append(Vec3(X,Y,Z))
               
            connectedRegionsIDs = map(int, portalNode.getTag("prop").split(','))   
      
            self.portals.append( Portal(connectedRegionsIDs, frontiers) )  
            
            self.convexRegions[ connectedRegionsIDs[0] - 1 ].neighbourIDs.append( connectedRegionsIDs[1] )
            self.convexRegions[ connectedRegionsIDs[0] - 1 ].portalsList.append( self.portals[-1] )
            self.convexRegions[ connectedRegionsIDs[1] - 1 ].neighbourIDs.append (connectedRegionsIDs[0] )
            self.convexRegions[ connectedRegionsIDs[1] - 1 ].portalsList.append( self.portals[-1] )
        # Debug    
#        for portal in self.portals: 
#            print portal.connectedRegionsIDs
