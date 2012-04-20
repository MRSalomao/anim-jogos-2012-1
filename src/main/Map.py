from pandac.PandaModules import *
from panda3d.bullet import BulletPlaneShape
from panda3d.bullet import BulletRigidBodyNode
from panda3d.bullet import BulletTriangleMesh
from panda3d.bullet import BulletTriangleMeshShape

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
        
