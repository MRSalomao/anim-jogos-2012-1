from pandac.PandaModules import *
from panda3d.bullet import BulletRigidBodyNode
from panda3d.bullet import BulletConvexHullShape
from direct.interval.IntervalGlobal import *
from direct.actor.Actor import Actor
from CharacterBody import *
from Creature import *
from math import *


import sys

class Enemy(Creature):
    
    def __init__(self, mainReference, name, position):
        self.mainRef = mainReference
        super(Enemy, self).__init__(mainReference)
        
        # unique enemy name
        self.name = name
        
        # enemy's pursue speed P-units/s
        self.speed = 1.2
        
        # enemy's rotation speed angles/s
        self.rotSpeed = 10
        
        # enemy's current convex region; for pursue purposes
        self.currentRegion = 1
        
        # Hit Points of each part of zombie
        self.hitPoints = {'leg_lr':2, 'leg_ll':2, 'arm_lr':2, 'arm_ll':2}
        self.lifePoints = 100
        
        # enemy NodePath
        self.enemyNP = self.mainRef.render.attachNewNode(self.name)
        self.enemyNP.setPos(position)
        
        # load our zombie
        self.enemyModel = Actor("../../models/model_zombie/zombie")
        # ****SCALE****
        self.enemyModel.setScale(0.55)
        # ****SCALE****
        
        #enemy's character controller
        self.enemyBody = CharacterBody(self.mainRef, self.enemyNP.getPos(), position.getZ(), position.getZ() )
        
        # load the zombie's bounding boxes
        self.enemyBB = loader.loadModel("../../models/model_zombie/zombieBB")
        
        global bodyParts      
        bodyParts = ['head', 'leg_ur', 'leg_ul', 'leg_lr', 'leg_ll', 'torso', 'arm_ur', 'arm_ul', 'arm_lr', 'arm_ll']
        
        # List of the bullet nodes for this enemy, to be removed later
        self.bulletNodes = {}
        self.partNodes = {}
        # Get Joints
        self.joints = {}
        
        for bodyPart in ['leg_lr', 'leg_ll', 'arm_lr', 'arm_ll']:
            # Get joint control structure
            self.joints[bodyPart] = self.enemyModel.controlJoint(None, 'modelRoot', bodyPart)
        
        # getting 1 by 1 and attaching them to their corresponding bones     
        for bodyPart in bodyParts:
            
            self.bodyPartShape = BulletConvexHullShape()
            self.bodyPartShape.addGeom(self.enemyBB.getChild(0).find(bodyPart).node().getGeom(0))
            
            self.bulletbodyPartNode = BulletRigidBodyNode(bodyPart+"_"+name)
            self.bulletbodyPartNode.addShape(self.bodyPartShape)
            self.bodyPartNode = self.mainRef.render.attachNewNode(self.bulletbodyPartNode)
            # ****SCALE****
            self.bodyPartNode.setScale(0.55)
            # ****SCALE****
            
            self.mainRef.world.attachRigidBody(self.bulletbodyPartNode)
            self.bodyPartNode.setCollideMask( BitMask32.bit( int(self.name.split('_')[1] ) ) )
       
            self.bodyPartNode.wrtReparentTo(self.enemyModel.exposeJoint(None,"modelRoot",bodyPart))
            
            self.bulletNodes[bodyPart] = self.bulletbodyPartNode
            self.partNodes[bodyPart] = self.bodyPartNode
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
        
        # walk loop
        self.enemyModel.loop("walk")
        
        # attaching to render
        self.enemyModel.reparentTo(self.enemyNP)
        
    def hide(self):
        self.enemyModel.hide()
        
    def show(self):
        self.mainRef.world.attachRigidBody(self.enemyBulletNode)
        self.enemyModel.show()
        self.enemyModel.loop("walk")
        
    def pursue(self):
        self.lostTargetTotalTime = 1.0

        self.lostTargetTimer = self.lostTargetTotalTime

        def pursueTargetStep(task):
            if (self.mainRef.player.currentRegion == self.currentRegion):
                
                targetDirection = Vec2( self.mainRef.player.playerNP.getPos(self.enemyNP).getXy() )
                targetDirectionAngle = Vec2(-sin(radians(self.enemyModel.getH())), 
                                             cos(radians(self.enemyModel.getH())) ).signedAngleDeg(targetDirection)

                rotationAngle = targetDirectionAngle * self.rotSpeed * globalClock.getDt()
                self.enemyModel.setH(self.enemyModel.getH() + rotationAngle)

                targetDirection.normalize()
                playerMoveSpeedVec = targetDirection * self.speed * globalClock.getDt()
                self.enemyNP.setPos( self.enemyBody.move(Vec3(playerMoveSpeedVec.getX(), playerMoveSpeedVec.getY(), 0) ) )                
                
                if (abs(rotationAngle) > 120 * globalClock.getDt()):
                    self.lostTargetTimer = self.lostTargetTotalTime
                    taskMgr.add(lostTargetStep, self.name + "lt")
                    return task.done
                 
            return task.cont
        
        def lostTargetStep(task):
            self.enemyNP.setPos( self.enemyBody.move(Vec3(-sin(radians(self.enemyModel.getH())) * self.speed * globalClock.getDt(),
                                                           cos(radians(self.enemyModel.getH())) * self.speed * globalClock.getDt(), 0) ) )
            self.lostTargetTimer -= globalClock.getDt()
            
            if (self.lostTargetTimer < 0):
                taskMgr.add(recoverTargetStep, self.name + "rt") 
                return task.done
            
            return task.cont
            
        def recoverTargetStep(task):
            targetDirection = Vec2( self.mainRef.player.playerNP.getPos(self.enemyNP).getXy() )
            targetDirectionAngle = Vec2(-sin(radians(self.enemyModel.getH())), 
                                         cos(radians(self.enemyModel.getH())) ).signedAngleDeg(targetDirection)

            rotationAngle = targetDirectionAngle * self.rotSpeed * globalClock.getDt()
            self.enemyModel.setH(self.enemyModel.getH() + rotationAngle)

            if (abs(targetDirectionAngle) < 5):
                taskMgr.add(pursueTargetStep, self.name + "pt") 
                return task.done
            
            return task.cont
                    
        taskMgr.add(pursueTargetStep, self.name + 'pt')
        
    def destroy(self):
        taskMgr.remove( str(self.name) )
        self.enemyModel.cleanup()
        self.enemyBB.removeNode()
        for node in self.bulletNodes.keys():
            self.mainRef.world.removeRigidBody(self.bulletNodes[node])
            
    def detachLimb(self,limb):
        # Detaches a limb from the enemy and makes it drop on the floor
        print "[Detach] Detach %s" % limb
        
#        self.partNodes[limb].wrtReparentTo(self.mainRef.render)
#
#        shape = BulletSphereShape(10.0)
#        node = BulletRigidBodyNode('Sphere')
#        node.setMass(1.0)
#        node.addShape(shape)
#        playerNP = self.mainRef.render.attachNewNode(node)
#        playerNP.setPos(self.enemyModel.exposeJoint(None,"modelRoot",limb).getPos())
#        playerNP.setPos(playerNP.getRelativePoint(self.partNodes[limb],self.partNodes[limb].getPos()))
#        playerNP.setPos(60,0,-60)
#        print playerNP.getRelativePoint(self.partNodes[limb],self.partNodes[limb].getPos())
#        print self.partNodes[limb].getPos()
#        self.mainRef.world.attachRigidBody(node)
#        
#        self.bulletNodes[limb].applyCentralForce(Vec3(0, 0, -5))
#        self.mainRef.world.removeRigidBody(self.bulletNodes[limb])

        