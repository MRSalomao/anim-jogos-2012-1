from main import Creature
from panda3d.bullet import BulletBoxShape
from pandac.PandaModules import *
from direct.actor.Actor import Actor
from panda3d.bullet import BulletWorld
from panda3d.bullet import BulletRigidBodyNode
from panda3d.bullet import BulletConvexHullShape
from panda3d.bullet import BulletDebugNode

from CharacterBody import *


import sys

class Enemy(Creature):
    
    def __init__(self, mainReference, name, position):
        self.mainRef = mainReference
        
        #unique enemy name
        self.name = name
        
        #enemy's pursue speed
        self.speed = 0.02
        
        #enemy's current convex region
        self.currentRegion = 1
        
        # path point as spawn point
        self.spawnP = None
        
        # Hit Points of each part of zombie
        self.hitPoints = {'leg_lr':2, 'leg_ll':2, 'arm_lr':2, 'arm_ll':2}
        self.lifePoints = 100
        
        # load our zombie
        self.enemyModel = Actor("../../models/model_zombie/zombie")
        # ****SCALE****
        self.enemyModel.setScale(0.4)
        # ****SCALE****
        self.enemyModel.setPos(position)
        
        #enemy's character controller
        self.enemyBody = CharacterBody(self.mainRef, Point3( self.enemyModel.getPos() ) , .4, .4) # Point3(self.enemyModel.getPos())
        
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
            #self.bulletbodyPartNode.setMass(1)
            #self.bulletbodyPartNode.setGravity(Vec3(0,0,0))
            self.bodyPartNode = self.mainRef.render.attachNewNode(self.bulletbodyPartNode)
            # ****SCALE****
            self.bodyPartNode.setScale(0.4)
            # ****SCALE****
            self.bodyPartNode.setPos(position)
            
            self.mainRef.world.attachRigidBody(self.bulletbodyPartNode)
       
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
        
        
#        self.enemyModel.setScale(20,20,20)
#        self.enemyModel.setPos(0,0,-80)  
        self.enemyModel.loop("walk")
        
        # Remove big box around enemy
        """self.enemyBulletShape = BulletBoxShape(Vec3(20,40,40))
        self.enemyBulletNode = BulletRigidBodyNode(name)
        self.enemyBulletNode.addShape(self.enemyBulletShape)
        self.np = self.mainRef.render.attachNewNode(self.enemyBulletNode)
        self.np.setPos(self.np.getZ()-10)
        self.mainRef.world.attachRigidBody(self.enemyBulletNode)
        self.enemyModel.reparentTo(self.np)"""
        self.enemyModel.wrtReparentTo(self.mainRef.render)

        
    def hide(self):
        ##self.mainRef.world.removeRigidBody(self.enemyBulletNode)
        #self.np.hide()
        self.enemyModel.hide()
        
    def show(self):
        self.mainRef.world.attachRigidBody(self.enemyBulletNode)
        #self.np.show()
        self.enemyModel.show()
        self.enemyModel.loop("walk")
        
    def setPos(self,x,y,z):
        #self.np.setPos(x,y,z)
        self.enemyModel.setPos(x,y,z)
        
    def pursue(self):
        def pursueStep(task):
            if (self.mainRef.player.currentRegion == self.currentRegion):
                enemyMovement = self.mainRef.camera.getPos().getXy() - self.enemyModel.getPos().getXy()
                enemyMovement.normalize()
                enemyMovement *= self.speed
                self.enemyModel.setPos( self.enemyBody.move(Vec3(enemyMovement.getX(), enemyMovement.getY(), 0) ) )
            return task.cont
        taskMgr.add(pursueStep, self.name)
        
#    def pursue(self,AIworld, pathPoints, playerWorldPos, xPosInterval,yPosInterval,zPosInterval):
#        # getting player positioning and assigning the closest grid point
#        playerPX = playerWorldPos.getX()
#        playerPY = playerWorldPos.getY()
#        playerPZ = playerWorldPos.getZ()
#        playerPathPoint = PathPoint(playerPX,playerPY,playerPZ)
#        currSquaredDist = sys.float_info.max
#        minSquaredDist = sys.float_info.max
#        bestGridPoint = None
#        for i in range(len(pathPoints)):
#            point = pathPoints[i]
#            currSquaredDist = playerPathPoint.getDistanceSquared(point)
#            if (minSquaredDist == sys.float_info.max):
#                minSquaredDist = playerPathPoint.getDistanceSquared(point)
#                bestGridPoint = point
#            if (currSquaredDist < minSquaredDist):
#                minSquaredDist = currSquaredDist
#                bestGridPoint = point
#        bestGridPoint # this point is the goal point for our PathFinder
#        
#        # testing path find
#        self.pFinder = PathFinder(AIworld, self.spawnP, 
#                                  PathPoint(bestGridPoint.X,bestGridPoint.Y,bestGridPoint.Z,None,bestGridPoint.gridPosX,bestGridPoint.gridPosY,bestGridPoint.gridPosZ),
#                                  pathPoints , xPosInterval, yPosInterval, zPosInterval)
#        crumb = self.pFinder.node
#        while (crumb != None):
#            # debug purposes
##            print crumb.point
#            #self.np.setPos(Point3(crumb.point.X,crumb.point.Y,crumb.point.Z))
#            self.enemyModel.setPos(Point3(crumb.point.X,crumb.point.Y,crumb.point.Z))
#
#            crumb = crumb.next
        
    def destroy(self):
#        self.enemyModel.unload()
#        self.enemyBB.unload()
        #self.np.detachNode()
        self.enemyModel.cleanup() #ou cleanup(). removeNode() para models.
        self.enemyBB.removeNode()
        for node in self.bulletNodes.keys():
            self.mainRef.world.removeRigidBody(self.bulletNodes[node])
            
    def detachLimb(self,limb):
        """ Detaches a limb from the enemy and makes it drop on the floor"""
        print "[Detach] Detach %s" % limb
        
        #self.partNodes[limb].wrtReparentTo(self.mainRef.render)

        #shape = BulletSphereShape(10.0)
        #node = BulletRigidBodyNode('Sphere')
        #node.setMass(1.0)
        #node.addShape(shape)
        #np = self.mainRef.render.attachNewNode(node)
        #np.setPos(self.enemyModel.exposeJoint(None,"modelRoot",limb).getPos())
        #np.setPos(np.getRelativePoint(self.partNodes[limb],self.partNodes[limb].getPos()))
        #np.setPos(60,0,-60)
        #print np.getRelativePoint(self.partNodes[limb],self.partNodes[limb].getPos())
        #print self.partNodes[limb].getPos()
        #self.mainRef.world.attachRigidBody(node)
        
        #self.bulletNodes[limb].applyCentralForce(Vec3(0, 0, -5))
        #self.mainRef.world.removeRigidBody(self.bulletNodes[limb])

        