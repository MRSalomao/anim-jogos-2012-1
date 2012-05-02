from pandac.PandaModules import *
from panda3d.bullet import BulletRigidBodyNode
from panda3d.bullet import BulletBoxShape
from panda3d.bullet import BulletCharacterControllerNode
from panda3d.bullet import BulletCapsuleShape
from panda3d.bullet import ZUp


from Creature import *
from MovementHandler import *

class Player(Creature):
    
    def __init__(self,mainReference):
        self.mainRef = mainReference
        super(Player, self).__init__(mainReference)
        
        # setting our bullet character node
        self.characterCapsuleHeight = 50
        self.characterCapsuleRadius = 4
        shape = BulletCapsuleShape(self.characterCapsuleRadius, self.characterCapsuleHeight, ZUp)
        
        self.playerNode = BulletCharacterControllerNode(shape, 0.4, 'Player')
        self.playerNP = self.mainRef.render.attachNewNode(self.playerNode)
        self.playerNP.setCollideMask(BitMask32.allOn())
        self.mainRef.world.attachCharacter(self.playerNP.node())
        self.mainRef.camera.reparentTo(self.playerNP)
        self.mainRef.camera.setPos(0,0,20)
        
        # setting our movementHandler
        self.movementHandler = MovementHandler(self.mainRef)
        self.movementHandler.registerFPSMovementInput() 

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

            direction = pTo - pFrom
            direction.normalize()
            result = self.mainRef.world.rayTestAll(pFrom, pFrom+direction*1000)
            if (result.hasHits()):
                self.mainRef.enemyManager.handleShot(result)
            
            # uncomment for projectile collision
#            # Calculate initial velocity
#            v = pTo - pFrom
#            v.normalize()
#            v *= 10000.0
#            
#            # Create bullet
#            shape = BulletBoxShape(Vec3(0.5, 0.5, 0.5))
#            body = BulletRigidBodyNode('Bullet')
#            bodyNP = render.attachNewNode(body)
#            bodyNP.node().addShape(shape)
#            bodyNP.node().setMass(0.001)
#            bodyNP.node().setLinearVelocity(v)
#            bodyNP.setPos(pFrom)
#            bodyNP.setCollideMask(BitMask32.allOn())
#            
#            # Enable CCD
#            bodyNP.node().setCcdMotionThreshold(1e-7)
#            bodyNP.node().setCcdSweptSphereRadius(0.50)
#            
#            self.mainRef.world.attachRigidBody(bodyNP.node())
#            
#            # Remove the bullet again after 1 second
#            bullets.append(bodyNP)
#            taskMgr.doMethodLater(1, removeBullet, 'removeBullet')
            
        # adding the shoot event
        self.mainRef.accept("mouse1", shootBullet)
        