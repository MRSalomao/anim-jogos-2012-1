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

        self.playerBody = CharacterBody(self.mainRef, Point3(0, 2, 1.7), .4, 1.7)
        
        # dummy nodepath for our player; we will attach everything to it
        
        # player bullet node
        playerNode = BulletRigidBodyNode('Player_NP') 
        playerNode.addShape( BulletCapsuleShape(0.3, 1, ZUp) ) # adicionar node no lugar da string
        self.mainRef.world.attachRigidBody(playerNode)
        
        self.playerNP = self.mainRef.render.attachNewNode(playerNode)
        # this collision mask will only avoid CharacterBody collision on itself
        self.playerNP.setCollideMask(BitMask32(0x7FFFFFFF))
        # notify collision contacts
        self.playerNP.node().notifyCollisions(True)
        
        self.mainRef.camera.reparentTo( self.playerNP )
        # eyes height
        self.mainRef.camera.setZ(0.2)
        
        # NodePath position
        self.playerNP.setPos(0,0,1.0)
        
        # setting our movementHandler
        self.movementHandler = MovementHandler(self.mainRef)
        self.movementHandler.registerFPSMovementInput()
        
        # attach default weapon
        self.activeWeapon = Glock(self.mainRef.camera)

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
            result = self.mainRef.world.rayTestClosest(pFrom, pFrom+direction*1000, mask = BitMask32.allOn() )
            if (result.hasHit()):
                self.mainRef.enemyManager.handleShot(result)
            # weapon anim
            self.activeWeapon.shootAnim()
            
        # adding the shoot event
        self.mainRef.accept("mouse1", shootBullet)
        
        # player boolean to authorize player HP decrease when zombie contact happens
        self.canLoseHP = True
        
    def onContactAdded(self, node1, node2):
        
        # decrease player's life when zombie contact happen
        if ( ( ('arm_ll' in node1.getName() ) or (node1.getName() == ('Player_NP') ) ) and 
             ( ('arm_ll' in node2.getName() ) or (node2.getName() == ('Player_NP') ) ) and
             ( self.canLoseHP ) ):
            
            # decrease player hp
            oldHPValue = int( self.mainRef.playerHUD.guiHp.node().getText() )
            if (oldHPValue > 0):
                decreasedHP = oldHPValue - 10
                self.mainRef.playerHUD.guiHp.node().setText( str(decreasedHP) )
                # block HP loss
                self.canLoseHP = False
                # schedule next HP loss release
                taskMgr.doMethodLater(1, self.releaseHPLoss, 'releaseHPLoss')
                # TODO: enemy animation call
                # TODO: screen effect player hurt
    
    def releaseHPLoss(self,task):
        self.canLoseHP = True
        task.done
       
        
        