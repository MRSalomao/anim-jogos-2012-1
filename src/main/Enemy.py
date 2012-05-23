from main import Creature
from panda3d.bullet import BulletBoxShape
from pandac.PandaModules import *
from direct.actor.Actor import Actor
from panda3d.bullet import BulletWorld
from panda3d.bullet import BulletRigidBodyNode
from panda3d.bullet import BulletConvexHullShape
from panda3d.bullet import BulletDebugNode

from pathfind.PathPoint import *
from pathfind import *

import sys

class Enemy(Creature):
    
    def __init__(self, mainReference, name):
        self.mainRef = mainReference
        
        #unique enemy name
        self.name = name
        
        # path point as spawn point
        self.spawnP = None
        
        # Hit Points of each part of zombie
        self.hitPoints = {'leg_lr':2, 'leg_ll':2, 'arm_lr':2, 'arm_ll':2}
        self.lifePoints = 100
        
        # load our zombie
        self.enemyModel = Actor("../../models/model_zombie/zombie")
        
        # load the zombie's bounding boxes
        self.enemyBB = loader.loadModel("../../models/model_zombie/zombieBB")
        
        global bodyParts      
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
        

        self.enemyBulletShape = BulletBoxShape(Vec3(20,40,40))
        self.enemyBulletNode = BulletRigidBodyNode(name)
        self.enemyBulletNode.addShape(self.enemyBulletShape)
        self.np = self.mainRef.render.attachNewNode(self.enemyBulletNode)
        self.np.setPos(self.np.getZ()-10)
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
        
    def pursue(self,AIworld, pathPoints, playerWorldPos, xPosInterval,yPosInterval,zPosInterval):
        # getting player positioning and assigning the closest grid point
        playerPX = playerWorldPos.getX()
        playerPY = playerWorldPos.getY()
        playerPZ = playerWorldPos.getZ()
        playerPathPoint = PathPoint(playerPX,playerPY,playerPZ)
        currSquaredDist = sys.float_info.max
        minSquaredDist = sys.float_info.max
        bestGridPoint = None
        for i in range(len(pathPoints)):
            point = pathPoints[i]
            currSquaredDist = playerPathPoint.getDistanceSquared(point)
            if (minSquaredDist == sys.float_info.max):
                minSquaredDist = playerPathPoint.getDistanceSquared(point)
                bestGridPoint = point
            if (currSquaredDist < minSquaredDist):
                minSquaredDist = currSquaredDist
                bestGridPoint = point
        bestGridPoint # this point is the goal point for our PathFinder
        
        # testing path find
        self.pFinder = PathFinder(AIworld, self.spawnP, 
                                  PathPoint(bestGridPoint.X,bestGridPoint.Y,bestGridPoint.Z,None,bestGridPoint.gridPosX,bestGridPoint.gridPosY,bestGridPoint.gridPosZ),
                                  pathPoints , xPosInterval, yPosInterval, zPosInterval)
        crumb = self.pFinder.node
        while (crumb != None):
            # debug purposes
#            print crumb.point
            self.np.setPos(Point3(crumb.point.X,crumb.point.Y,crumb.point.Z))
            crumb = crumb.next
        
    def destroy(self):
#        self.enemyModel.unload()
#        self.enemyBB.unload()
        self.np.detachNode()