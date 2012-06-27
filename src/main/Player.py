from pandac.PandaModules import *
from panda3d.bullet import BulletRigidBodyNode
from panda3d.bullet import BulletBoxShape
from panda3d.bullet import BulletSphereShape
from panda3d.bullet import BulletCapsuleShape
from panda3d.bullet import BulletCylinderShape
from panda3d.bullet import ZUp
from CharacterBody import *

from Glock import *
from Creature import *
from MovementHandler import *

class Player(Creature):
    
    def __init__(self,mainReference):
        self.mainRef = mainReference
        super(Player, self).__init__(mainReference)
        
        # setting player HP
        self.healthPoints = 100
        
        # fine tuning the camera properties
        self.mainRef.camLens.setFov(50)
        self.mainRef.camLens.setNear(0.02)
        self.mainRef.camLens.setFar(80.0)
        
        self.currentRegion = 1

        self.playerBody = CharacterBody(self.mainRef, Point3(0, 2, 3), .4, 1.2)
        
        # dummy nodepath for our player; we will attach everything to it
        
#        node = BulletRigidBodyNode('Player_NP') 
#        node.addShape( BulletCapsuleShape(.8, 1.0, ZUp) ) # adicionar node no lugar da string
        self.np = self.mainRef.render.attachNewNode('Player_Node')
        
#        self.mainRef.camera.setPos(0, 0, 1.0)
        self.mainRef.camera.wrtReparentTo( self.np )
        self.np.setPos(0,0,1.0)
        
        # setting our movementHandler
        self.movementHandler = MovementHandler(self.mainRef)
        self.movementHandler.registerFPSMovementInput()
        
        # attach default weapon
        self.activeWeapon = Glock(self.np)

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
            result = self.mainRef.world.rayTestClosest(pFrom, pFrom+direction*1000)
            if (result.hasHit()):
                self.mainRef.enemyManager.handleShot(result)
            # weapon anim
            self.activeWeapon.shootAnim()
            
        # adding the shoot event
        self.mainRef.accept("mouse1", shootBullet)
        
       
        
        