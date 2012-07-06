from pandac.PandaModules import *
from panda3d.bullet import BulletRigidBodyNode
from panda3d.bullet import BulletBoxShape
from panda3d.bullet import BulletSphereShape
from panda3d.bullet import BulletCapsuleShape
from panda3d.bullet import BulletCylinderShape
from panda3d.bullet import ZUp
from direct.showbase import Audio3DManager

from math import *

from CharacterBody import *
from direct.particles.ParticleEffect import ParticleEffect

from Glock import *
from Creature import *
from PlayerMovementHandler import *


class Player(Creature):
    
    def __init__(self,mainReference):
        
        super(Player, self).__init__(mainReference)
        
        # setting player HP
        self.healthPoints = 100
        
        # fine tuning the camera properties
        self.mainRef.camLens.setFov(50)
        self.mainRef.camLens.setNear(0.02)
        self.mainRef.camLens.setFar(80.0)
        
        self.currentRegionID = 1

        # dummy nodepath for our player; we will attach everything to it
        
        # player bullet node - NOTE: for detecting collision with attacks, only
        playerNode = BulletRigidBodyNode() 
        playerNode.addShape( BulletCapsuleShape(0.3, 1, ZUp) ) # adicionar node no lugar da string
        self.mainRef.world.attachRigidBody(playerNode)
        
        self.playerNP = self.mainRef.render.attachNewNode(playerNode)
        # this collision mask will only avoid CharacterBody collision on itself
        self.playerNP.setCollideMask(BitMask32(0x7FFFFFFF))
        # notify collision contacts
        self.playerNP.node().notifyCollisions(True)
        
        
        self.playerHeadNP = NodePath("empty") # This node is intended to be a placeholder for the camera (maintainability only)
        
        self.playerHeadNP.reparentTo( self.playerNP )
                
#        self.mainRef.camera.setPos(0, -4, 0)
        self.mainRef.camera.reparentTo( self.playerHeadNP )
        
        
        # NodePath position
        self.playerNP.setPos(0,0,1.0)
        
        # setting player's character body
        self.playerBody = CharacterBody(self.mainRef, self.playerNP.getPos(), .4, 1.0)
        self.playerBody.charBodyNP.reparentTo(self.playerNP) 
        
        # setting our movementHandler
        self.movementHandler = MovementHandler(self.mainRef)
        self.movementHandler.registerFPSMovementInput()
        
        # attach default weapon
        self.activeWeapon = Glock(self.mainRef.camera)

        def shootBullet():
            pTo = Vec3(-sin(radians(self.playerHeadNP.getH())) * cos(radians(self.playerHeadNP.getP())), 
                       cos(radians(self.playerHeadNP.getH())) * cos(radians(self.playerHeadNP.getP())), 
                       sin(radians(self.playerHeadNP.getP())) )

            result = self.mainRef.world.rayTestClosest(self.playerNP.getPos(), self.playerNP.getPos() + (pTo * 100.0), mask = BitMask32.allOn() )
            if (result.hasHit()):
                self.mainRef.enemyManager.handleShot(result)
                
            # weapon anim
            self.activeWeapon.shootAnim()
            
            # playing shoot sound
            glockShot = self.mainRef.loadSfx("../../sounds/glock_single_shot.mp3")
            glockShot.setVolume(0.2)
            glockShot.play()
            
        # adding the shoot event
        self.mainRef.accept("mouse1", self.shootBullet)
        
        # player boolean to authorize player HP decrease when zombie contact happens
        self.canLoseHP = True


    def shootParticles(self,collision_result):
        "Summons and explosion of particles where the player shot."
        # Create Particle
        p = ParticleEffect()
        p.loadConfig("../../models/particle_shot.ptf")
        
        # Put particle at shot point
        p.setPos(collision_result.getHitPos())        
        p.start(parent = self.mainRef.render, renderParent = self.mainRef.render)

        # Schedule particle effect cleanup
        particle_timeout = 0.2 # Time in seconds for the particle effect to fade
        taskMgr.doMethodLater(particle_timeout, self.releaseParticle, 'Particle Effect Cleanup', extraArgs = [p])



    def shootBullet(self):
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

        # Shoot particles
        self.shootParticles(result)

        if (result.hasHit()):
            self.mainRef.enemyManager.handleShot(result)
        # weapon anim
        self.activeWeapon.shootAnim()
        
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
       
    def releaseParticle(self,particle_system):
        "Cleanup particle effect after timeout"
        particle_system.cleanup()
        
        