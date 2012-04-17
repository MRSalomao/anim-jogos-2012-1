from pandac.PandaModules import *
from panda3d.bullet import BulletRigidBodyNode
from panda3d.bullet import BulletBoxShape

from Creature import *

class Player(Creature):
    
    def __init__(self,mainReference):
        self.mainRef = mainReference
        super(Player, self).__init__(mainReference)
        
        # player collision box
        self.playerBulletNode = BulletRigidBodyNode('player')
        self.playerBulletNode.addShape(BulletBoxShape(Vec3(10,10,10)))
        self.np = self.mainRef.render.attachNewNode(self.playerBulletNode)
        self.mainRef.world.attachRigidBody(self.playerBulletNode)
        self.npPlayerCamBox = self.mainRef.camera.attachNewNode(self.playerBulletNode)
        
        # adding bullets when pressing left btn mouse
        bullets = []
        def removeBullet(task):
            if len(bullets) < 1: return
            
            bulletNP = bullets.pop(0)
            self.mainRef.world.removeRigidBody(bulletNP.node())
            
            return task.done

        def shootBullet():
            # Get from/to points from mouse click
            pMouse = base.mouseWatcherNode.getMouse()
            pFrom = Point3()
            pTo = Point3()
            base.camLens.extrude(pMouse, pFrom, pTo)
            
            pFrom = render.getRelativePoint(base.cam, pFrom)
            pTo = render.getRelativePoint(base.cam, pTo)
            
            # Calculate initial velocity
            v = pTo - pFrom
            v.normalize()
            v *= 10000.0
            
            # Create bullet
            shape = BulletBoxShape(Vec3(0.5, 0.5, 0.5))
            body = BulletRigidBodyNode('Bullet')
            bodyNP = render.attachNewNode(body)
            bodyNP.node().addShape(shape)
            bodyNP.node().setMass(0.001)
            bodyNP.node().setLinearVelocity(v)
            bodyNP.setPos(pFrom)
            bodyNP.setCollideMask(BitMask32.allOn())
            
            # Enable CCD
            bodyNP.node().setCcdMotionThreshold(1e-7)
            bodyNP.node().setCcdSweptSphereRadius(0.50)
            
            self.mainRef.world.attachRigidBody(bodyNP.node())
            
            # Remove the bullet again after 1 second
            bullets.append(bodyNP)
            taskMgr.doMethodLater(1, removeBullet, 'removeBullet')
            
        # adding the shoot event
        self.mainRef.accept("mouse1", shootBullet)