from main import Creature
from panda3d.bullet import BulletBoxShape
from pandac.PandaModules import *
from direct.actor.Actor import Actor
from panda3d.bullet import BulletWorld
from panda3d.bullet import BulletRigidBodyNode
from panda3d.bullet import BulletConvexHullShape
from panda3d.bullet import BulletDebugNode

class Enemy(Creature):
    
    def __init__(self, mainReference, name):
        self.mainRef = mainReference
        
        # load our zombie
        self.enemyModel = Actor("../../models/model_zombie/zombie")
        
        # load the zombie's bounding boxes
        self.enemyBB = loader.loadModel("../../models/model_zombie/zombieBB")
                
        bodyParts = ['head', 'leg_ur', 'leg_ul', 'leg_lr', 'leg_ll', 'torso', 'arm_ur', 'arm_ul', 'arm_lr', 'arm_ll']
                
        # getting 1 by 1 and attaching them to their corresponding bones     
        for bodyPart in bodyParts:

            self.bodyPartShape = BulletConvexHullShape()
            self.bodyPartShape.addGeom(self.enemyBB.getChild(0).find(bodyPart).node().getGeom(0))
            
            self.bulletbodyPartNode = BulletRigidBodyNode(bodyPart)
            self.bulletbodyPartNode.addShape(self.bodyPartShape)
            
            self.bodyPartNode = self.mainRef.render.attachNewNode(self.bulletbodyPartNode)
            self.mainRef.world.attachRigidBody(self.bulletbodyPartNode)
       
            self.bodyPartNode.wrtReparentTo(self.enemyModel.exposeJoint(None,"modelRoot",bodyPart))
            
            # uncomment to use triangleMesh instead of convexHull
#            mesh = BulletTriangleMesh()
#            mesh.addGeom(self.enemyBB.getChild(0).find(bodyPart).node().getGeom(0))
#            self.bodyPartShape = BulletTriangleMeshShape(mesh, dynamic=True)
#            
#            self.bulletbodyPartNode = BulletRigidBodyNode(bodyPart)
#            self.bulletbodyPartNode.addShape(self.bodyPartShape)
#            
#            self.bodyPartNode = self.mainRef.render.attachNewNode(self.bulletbodyPartNode)
#            self.mainRef.world.attachRigidBody(self.bulletbodyPartNode)
#       
#            self.bodyPartNode.wrtReparentTo(self.enemyModel.exposeJoint(None,"modelRoot",bodyPart))
        
        
           
        self.enemyModel.setScale(20,20,20)
        self.enemyModel.setZ(-60)  
        

        self.enemyBulletShape = BulletBoxShape(Vec3(12,12,12))
        self.enemyBulletNode = BulletRigidBodyNode(name)
        self.enemyBulletNode.addShape(self.enemyBulletShape)
        self.np = self.mainRef.render.attachNewNode(self.enemyBulletNode)
        self.mainRef.world.attachRigidBody(self.enemyBulletNode)
        self.enemyModel.reparentTo(self.np)
        self.enemyModel.loop("walk")
        
    def hide(self):
        self.mainRef.world.removeRigidBody(self.enemyBulletNode)
        self.np.hide()
        
    def show(self):
        self.mainRef.world.attachRigidBody(self.enemyBulletNode)
        self.np.show()
        self.enemyModel.loop("walk")
        
    def setPos(self,x,y,z):
        self.np.setPos(x,y,z)