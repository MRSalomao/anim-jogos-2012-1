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
        
        self.tex = loader.loadTexture("../../models/floorlm.png")
        self.tsf = TextureStage('ts')
        self.tsf.setMode(TextureStage.MModulate)
        self.tsf.setTexcoordName("ul")      
        self.floor = self.testRoom.getChild(0).getChild(0)
        self.floor.setTexture(self.tsf, self.tex)
        
        self.tex = loader.loadTexture("../../models/floorlm.png")
        self.tsf = TextureStage('ts')
        self.tsf.setMode(TextureStage.MModulate)
        self.tsf.setTexcoordName("ul")      
        self.floor = self.testRoom.getChild(0).getChild(3)
        self.floor.setTexture(self.tsf, self.tex)
        
        self.tex2 = loader.loadTexture("../../models/wall2lm.png")
        self.tsw1 = TextureStage('ts1')
        self.tsw1.setMode(TextureStage.MModulate)
        self.tsw1.setTexcoordName("ul")      
        self.wall1 = self.testRoom.getChild(0).getChild(4)
        self.wall1.setTexture(self.tsw1, self.tex2)
        
        self.tex3 = loader.loadTexture("../../models/wall1lm.jpg")
        self.tsf1 = TextureStage('ts2')
        self.tsf1.setMode(TextureStage.MModulate)
        self.tsf1.setTexcoordName("ul")      
        self.floor = self.testRoom.getChild(0).getChild(2)
        self.floor.setTexture(self.tsf1, self.tex3)
        
        self.tex4 = loader.loadTexture("../../models/floor2lm.png")
        self.tsf2 = TextureStage('ts3')
        self.tsf2.setMode(TextureStage.MModulate)
        self.tsf2.setTexcoordName("ul")      
        self.floor = self.testRoom.getChild(0).getChild(1)
        self.floor.setTexture(self.tsf2, self.tex4)
        
        # map physics plane - flat infinite plane surface
#        shape = BulletPlaneShape(Vec3(0, 0, 1), 1)
#        node = BulletRigidBodyNode('Ground')
#        node.addShape(shape)
#        np = render.attachNewNode(node)
#        np.setPos(0, 0, -68)
#        self.mainRef.world.attachRigidBody(node)