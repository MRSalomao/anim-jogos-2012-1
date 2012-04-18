from pandac.PandaModules import *
from panda3d.bullet import BulletRigidBodyNode
from panda3d.bullet import BulletBoxShape

from main import Creature

class Enemy(Creature):
    
    def __init__(self, mainReference, name):
        self.mainRef = mainReference
        super(Enemy, self).__init__(mainReference)
        
        self.enemyModel = loader.loadModel("../../models/watermelon")
        self.enemyModel.setScale(7,7,7)
        self.enemyModel.setHpr(90,0,90)
        self.enemyGeomNodes = self.enemyModel.findAllMatches('**/+GeomNode')
        self.enemyGeomNode = self.enemyGeomNodes.getPath(0).node()
        self.enemyGeom = self.enemyGeomNode.getGeom(0)
        self.enemyBulletShape = BulletBoxShape(Vec3(12,12,12))
#        self.enemyBulletShape.addGeom(self.enemyGeom)
        self.enemyBulletNode = BulletRigidBodyNode(name)
#        self.enemyBulletNode.setMass(4)
        self.enemyBulletNode.addShape(self.enemyBulletShape)
        self.np = self.mainRef.render.attachNewNode(self.enemyBulletNode)
        self.mainRef.world.attachRigidBody(self.enemyBulletNode)
        self.enemyModel.flattenLight()
        self.enemyModel.reparentTo(self.np)
        
    def hide(self):
        self.mainRef.world.removeRigidBody(self.enemyBulletNode)
        self.np.hide()
    def show(self):
        self.mainRef.world.attachRigidBody(self.enemyBulletNode)
        self.np.show()
    def setPos(self,x,y,z):
        self.np.setPos(x,y,z)