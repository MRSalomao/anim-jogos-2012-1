from pandac.PandaModules import *
from panda3d.bullet import BulletRigidBodyNode
from panda3d.bullet import BulletConvexHullShape
from direct.interval.IntervalGlobal import *
from direct.actor.Actor import Actor
from CharacterBody import *
from Creature import *
from math import *


import sys
import random

class Enemy(Creature):
    
    def __init__(self, mainReference, name, position, regionID):
        
        super(Enemy, self).__init__(mainReference)
        
        # unique enemy name
        self.name = name
        
        # If enemy is alive
        self.alive = True
        
        # enemy's pursue speed P-units/s
        self.speed = 2.9
        
        # enemy's rotation speed angles/s
        self.rotSpeed = 10
        
        # enemy's current convex region; for pursue purposes
        self.currentRegionID = regionID
        
        # Hit Points of each part of zombie
        self.hitPoints = {'leg_lr':2, 'leg_ll':2, 'arm_lr':2, 'arm_ll':2}
        self.lifePoints = 100
        
        # enemy NodePath
        self.enemyNP = self.mainRef.render.attachNewNode(self.name)
        self.enemyNP.setPos(position)
        
        # the name of the task the zombie is currently performing
        self.enemyActiveState = ""
        
        self.isEnemyAttacking = False
        
        # the cross point of the portal that the zombie is trying to cross
        self.currentCrossPointGoal = None
        
        # the time that the enemy will spend confused
        self.lostTargetTotalTime = 1.0
        self.lostTargetTimer = self.lostTargetTotalTime
        
        # load our zombie
        self.enemyModel = Actor("../../models/model_zombie/zombie",{
                                'walk':'../../models/model_zombie/zombie-walk',
                                'attack':'../../models/model_zombie/zombie-attack',
})
        # ****SCALE****
        self.enemyModel.setScale(0.55)
        # ****SCALE****
        
        #enemy's character controller
        self.enemyBody = CharacterBody(self.mainRef, self.enemyNP.getPos(), 0.38, 0.5 )
        self.enemyBody.charBodyNP.reparentTo(self.enemyNP)
        
        # load the zombie's bounding boxes
        self.enemyBB = loader.loadModel("../../models/model_zombie/zombieBB")
        
        global bodyParts      
        bodyParts = ['head', 'leg_ur', 'leg_ul', 'leg_lr', 'leg_ll', 'torso', 'arm_ur', 'arm_ul', 'arm_lr', 'arm_ll']
        
        # List of the bullet nodes for this enemy, to be removed later
        self.bulletNodes = {}
        self.partNodes = {}
        # Get Joints
        self.joints = {}
        
        #for bodyPart in ['leg_lr', 'leg_ll', 'arm_lr', 'arm_ll']:
        #    # Get joint control structure
        #    self.joints[bodyPart] = self.enemyModel.controlJoint(None, 'modelRoot', bodyPart)
        
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
            self.bodyPartNode.setCollideMask( BitMask32.bit( 2 ) )
       
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

        # initial path must be calculated
        self.updatePath()
        
        # adding a task to check if the enemy is leaving their region
        self.checkIfChangedRegionName = self.name + "cicr"
        self.oldPosition = self.enemyNP.getPos()
        taskMgr.add(self.checkIfChangedRegion, self.checkIfChangedRegionName)
        
        # walk loop
#        self.enemyModel.loop("walk")
        self.enemyModel.loop("walk")
        
        # attaching to render
        self.enemyModel.reparentTo(self.enemyNP)
        self.enemyModel.setPos(0,0,-0.51)
        
        # loading enemy roar sound
        zombieRoar = [None,None,None,None]
        for i in range( len(zombieRoar) ):
            zombieRoar[i] = self.mainRef.audio3d.loadSfx('../../sounds/zombie_roar_' + str(i+1) + '.mp3')
        # initialize first zombie roar
        self.zombieRoarFX = zombieRoar[0] 
        self.mainRef.audio3d.attachSoundToObject(self.zombieRoarFX, self.enemyNP)
        self.zombieRoarFX.play()
        # random zombie roar
        def roarSort(task):
            if(self.zombieRoarFX.status() != self.zombieRoarFX.PLAYING):
                random.seed()
                value = random.choice(range(3))
                self.zombieRoarFX = zombieRoar[value]
                self.mainRef.audio3d.attachSoundToObject(self.zombieRoarFX, self.enemyNP)
                self.zombieRoarFX.play()
            return task.again
        self.mainRef.taskMgr.doMethodLater(2, roarSort,self.name+'roar sort')
        
    def hide(self):
        self.enemyModel.hide()
        
    def show(self):
        self.mainRef.world.attachRigidBody(self.enemyBulletNode)
        self.enemyModel.show()
        self.enemyModel.loop("walk")
        
    
    def setNewCourse(self):
        # Simply follow the player
        if (len(self.portalsPathList) == 0):
            taskMgr.remove( self.enemyActiveState )
            self.enemyActiveState = self.name + "pt"
            taskMgr.add(self.pursueTargetStep, self.enemyActiveState)

        
        # Go to the cross point that makes you closer to your target
        elif (self.portalsPathList[0].connectedRegionsIDs[0] == self.mainRef.player.currentRegionID or
              self.portalsPathList[0].connectedRegionsIDs[1] == self.mainRef.player.currentRegionID):
            
            self.setOptimalCrossPoint()
            
            taskMgr.remove( self.enemyActiveState )
            self.enemyActiveState = self.name + "htp"
            taskMgr.add(self.headToPortalStep, self.enemyActiveState)
        
        
        # Go to the middle cross point
        else:
            
            self.currentCrossPointGoal = self.portalsPathList[0].middleCrossPoint
            
            taskMgr.remove( self.enemyActiveState )
            self.enemyActiveState = self.name + "htp"
            taskMgr.add(self.headToPortalStep, self.enemyActiveState)
            
    #                 ======================================================================== 
    #                 ======================== STATE MACHINE METHODS ==========================        
    def pursueTargetStep(self, task):
        if (self.mainRef.player.currentRegionID == self.currentRegionID):
            
            if ( self.mainRef.player.playerNP.getPos(self.enemyNP).length() < 4.0):
                if (not self.isEnemyAttacking):
                    self.speed += 1.0
                    self.isEnemyAttacking = True
                    self.enemyModel.loop("attack")     
                                   
            elif (self.isEnemyAttacking):
                self.speed -= 1.0
                self.isEnemyAttacking = False
                self.enemyModel.loop("walk") 
            
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
                self.enemyActiveState = self.name + "lt"
                taskMgr.add(self.lostTargetStep, self.enemyActiveState)
                return task.done
             
        return task.cont
    
    def lostTargetStep(self, task):
        self.enemyNP.setPos( self.enemyBody.move(Vec3(-sin(radians(self.enemyModel.getH())),
                                                       cos(radians(self.enemyModel.getH())),
                                                        0) * self.speed * globalClock.getDt() ) )
        self.lostTargetTimer -= globalClock.getDt()
        
        if (self.lostTargetTimer < 0):
            self.enemyActiveState = self.name + "rt"
            taskMgr.add(self.recoverTargetStep, self.enemyActiveState) 
            return task.done
        
        return task.cont
        
    def recoverTargetStep(self, task):
        targetDirection = Vec2( self.mainRef.player.playerNP.getPos(self.enemyNP).getXy() )
        targetDirectionAngle = Vec2(-sin(radians(self.enemyModel.getH())), 
                                     cos(radians(self.enemyModel.getH())) ).signedAngleDeg(targetDirection)

        rotationAngle = targetDirectionAngle * self.rotSpeed * globalClock.getDt()
        self.enemyModel.setH(self.enemyModel.getH() + rotationAngle)

        if (abs(targetDirectionAngle) < 5):
            self.enemyActiveState = self.name + "pt"
            taskMgr.add(self.pursueTargetStep, self.enemyActiveState) 
            return task.done
        
        return task.cont
    
    def headToPortalStep(self, task):
        directionVec = Vec3(self.currentCrossPointGoal.getX() - self.enemyNP.getX(),
                            self.currentCrossPointGoal.getY() - self.enemyNP.getY(), 0)
        directionVec.normalize()
        
        targetDirection = Vec2( self.currentCrossPointGoal - self.enemyNP.getPos().getXy() )
        targetDirectionAngle = Vec2(-sin(radians(self.enemyModel.getH())), 
                                     cos(radians(self.enemyModel.getH())) ).signedAngleDeg(targetDirection)

        rotationAngle = targetDirectionAngle * self.rotSpeed * globalClock.getDt()
        self.enemyModel.setH(self.enemyModel.getH() + rotationAngle)
        
        self.enemyNP.setPos( self.enemyBody.move( directionVec * self.speed * globalClock.getDt() ) )
        
        return task.cont    
    #              ====================== END OF STATE MACHINE METHODS ========================  
    #              ============================================================================
        
    def destroy(self):
        self.alive = False
        taskMgr.remove(self.name+'roar sort') # removing sound
        for node in self.bulletNodes.keys():
            self.mainRef.world.removeRigidBody(self.bulletNodes[node])
            self.partNodes[node].removeNode()
        taskMgr.remove( self.enemyActiveState ) # removing state machine task 
        self.enemyModel.cleanup()
        self.enemyBB.removeNode()
        self.enemyBody.destroy()

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

    def updatePath(self):
        
        convexRegionsList = self.mainRef.map.convexRegions      
        self.portalsPathList = []        # this is what we want for enemy's correct pursue path
        discoveredRegionsList = []     # part of the BFS algorithm
        visitedRegionsList = [False for item in range( len(convexRegionsList))]
        regionFatherList = [None for item in range( len(convexRegionsList))]       # this list keeps track of a region's father AND the portalEntrance connecting them
        
        # from now, we'll execute a BFS to find each region that enemy will cross to reach player's position
        discoveredRegionsList.append( convexRegionsList[self.currentRegionID] )
        visitedRegionsList[self.currentRegionID] = True
        regionFatherList[self.currentRegionID] = [-1, None]
        
        while(discoveredRegionsList):
            
            analisedRegion = discoveredRegionsList.pop(0)
            for portalEntrance in analisedRegion.portalEntrancesList:
                neighbourRegionID = portalEntrance.connectedRegionID
                
                if (not visitedRegionsList[neighbourRegionID]):
                    regionFatherList[neighbourRegionID] = [analisedRegion.regionID, portalEntrance.portal]
                    
                    if (neighbourRegionID == self.mainRef.player.currentRegionID):
                        discoveredRegionsList = [] # break while statement trick          
                        break
                    
                    visitedRegionsList[neighbourRegionID] = True
                    discoveredRegionsList.append( convexRegionsList[neighbourRegionID] )
        
        # now that we have all regions necessary , we'll just put all portals on the correct order
        lastRegionFatherID = self.mainRef.player.currentRegionID
        while (lastRegionFatherID != -1):
            lastRegionFather = regionFatherList[lastRegionFatherID]
            lastRegionFatherID = lastRegionFather[0]
            self.portalsPathList.append(lastRegionFather[1])
        
        # putting portals path on the right order for enemy pursuing algorithm
        self.portalsPathList.pop()  
        self.portalsPathList.reverse()
        
        # Debug
#        print "lista de portais:"
#        for portal in self.portalsPathList:
#            print portal.connectedRegionsIDs

        self.setNewCourse()

    def checkIfChangedRegion(self, task, lastRegion=0):
        
        for portalEntrance in self.mainRef.map.convexRegions[self.currentRegionID].portalEntrancesList:
            
            if ( self.intersect( self.oldPosition, self.enemyNP.getPos(), 
                                 portalEntrance.portal.frontiers[0], portalEntrance.portal.frontiers[1] )
                                 and portalEntrance.portal.connectedRegionsIDs[0] != lastRegion 
                                 and portalEntrance.portal.connectedRegionsIDs[1] != lastRegion ):
                
                oldRegion = self.mainRef.player.currentRegionID
                self.currentRegionID = portalEntrance.connectedRegionID

                
                # Debug
#                print self.name + " region changed: ", oldRegion, ">", self.currentRegionID
                
                # erase last item of portalsPathList (if it isn't empty)
                if (len(self.portalsPathList) != 0):
                    self.portalsPathList.pop(0)
                
                # new course must be calculated if the enemy changed it's region
                self.setNewCourse()
        
        self.oldPosition = self.enemyNP.getPos()
        
        return task.cont        

    def ccw(self, A,B,C):
        return (C.getY()-A.getY())*(B.getX()-A.getX()) > (B.getY()-A.getY())*(C.getX()-A.getX())
    
    def intersect(self, A,B,C,D):
        return self.ccw(A,C,D) != self.ccw(B,C,D) and self.ccw(A,B,C) != self.ccw(A,B,D)



    def setOptimalCrossPoint(self):
        
        deltaPositionVec = self.mainRef.player.playerNP.getPos() - self.enemyNP.getPos()
        positionPoint = self.enemyNP.getPos()
        
        deltaFrontiersVec = self.portalsPathList[0].frontiersVec
        frontierPoint = self.portalsPathList[0].frontiers[0]
        
        if (deltaPositionVec.getX() == 0):
            tang2 = deltaFrontiersVec.getY() / deltaFrontiersVec.getX()
            b2 = frontierPoint.getY() - tang2 * frontierPoint.getX()
            
            xRes = positionPoint.getX()
            yRes = tang2 * xRes + b2
            
            
        if (deltaFrontiersVec.getX() == 0):
            tang1 = deltaPositionVec.getY() / deltaPositionVec.getX()
            b1 = positionPoint.getY() - tang1 * positionPoint.getX()
            
            xRes = frontierPoint.getX()
            yRes = tang1 * xRes + b1
            
        
        else:
            tang1 = deltaPositionVec.getY() / deltaPositionVec.getX()
            tang2 = deltaFrontiersVec.getY() / deltaFrontiersVec.getX()
            
            b1 = positionPoint.getY() - tang1 * positionPoint.getX()
            b2 = frontierPoint.getY() - tang2 * frontierPoint.getX()
            
            xRes = (b1 - b2) / (tang1 - tang2)
            yRes = tang1 * xRes + b1
            
            
        if (deltaFrontiersVec.getX() == 0):
            if ( ( yRes > self.portalsPathList[0].crossPoints[0].getY() and yRes < self.portalsPathList[0].crossPoints[1].getY() ) or
                 ( yRes < self.portalsPathList[0].crossPoints[0].getY() and yRes > self.portalsPathList[0].crossPoints[1].getY() ) ) :
                self.currentCrossPointGoal = Vec2(xRes, yRes)
                
            elif (yRes > self.portalsPathList[0].crossPoints[0].getY() and
                  yRes > self.portalsPathList[0].crossPoints[1].getY() ):
                if ( self.portalsPathList[0].crossPoints[0].getY() > 
                     self.portalsPathList[0].crossPoints[1].getY()):
                    self.currentCrossPointGoal = self.portalsPathList[0].crossPoints[0]
                else:
                    self.currentCrossPointGoal = self.portalsPathList[0].crossPoints[1]
        
            else:
                if ( self.portalsPathList[0].crossPoints[0].getY() < 
                     self.portalsPathList[0].crossPoints[1].getY()):
                    self.currentCrossPointGoal = self.portalsPathList[0].crossPoints[0]
                else:
                    self.currentCrossPointGoal = self.portalsPathList[0].crossPoints[1]
         
         
        else:
            if ( ( xRes > self.portalsPathList[0].crossPoints[0].getX() and xRes < self.portalsPathList[0].crossPoints[1].getX() ) or
                 ( xRes < self.portalsPathList[0].crossPoints[0].getX() and xRes > self.portalsPathList[0].crossPoints[1].getX() ) ) :
                self.currentCrossPointGoal = Vec2(xRes, yRes)
                
            elif (xRes > self.portalsPathList[0].crossPoints[0].getX() and
                  xRes > self.portalsPathList[0].crossPoints[1].getX()):
                if ( self.portalsPathList[0].crossPoints[0].getX() > 
                     self.portalsPathList[0].crossPoints[1].getX()):
                    self.currentCrossPointGoal = self.portalsPathList[0].crossPoints[0]
                else:
                    self.currentCrossPointGoal = self.portalsPathList[0].crossPoints[1]
        
            else:
                if ( self.portalsPathList[0].crossPoints[0].getX() < 
                     self.portalsPathList[0].crossPoints[1].getX()):
                    self.currentCrossPointGoal = self.portalsPathList[0].crossPoints[0]
                else:
                    self.currentCrossPointGoal = self.portalsPathList[0].crossPoints[1]




        