from panda3d.bullet import *
from pandac.PandaModules import *

class CharacterBody(object):
    
    def __init__(self, mainReference, initialPosition, bodyRadius, bodyHeight):
        self.mainRef = mainReference
        self.position = initialPosition
        self.bodyRadius = bodyRadius
        self.bodyHeight = bodyHeight
        self.stepNormal = ZUp
        
        # character body's sphere shape
        self.charBodySphereShape = BulletSphereShape(bodyRadius)
        self.charBodySphereShapeMinor = BulletSphereShape(bodyRadius - 0.1)
        
        self.collisionNode = BulletRigidBodyNode()
        self.collisionNode.addShape(self.charBodySphereShape)
        self.mainRef.world.attachRigidBody(self.collisionNode)
        
        self.charBodyNP = self.mainRef.render.attachNewNode(self.collisionNode)
        # this collision mask will only avoid CharacterBody collision on itself
        self.charBodyNP.setCollideMask(BitMask32(0x7FFFFFFF))
        
        self.accelerationStep = -9.81 / 60.0
        self.fallingSpeed = Vec3(0,0,0)

        
    def move(self, speedVec):
        self.tryToMoveXY(speedVec)
        self.tryToMoveZ(speedVec)
        return self.position
        
    def tryToMoveXY(self, speedVec):
        newPositionAttempt = self.position + speedVec     
        result = self.mainRef.world.sweepTestClosest(self.charBodySphereShape, 
                                                     TransformState.makePos(self.position), 
                                                     TransformState.makePos(newPositionAttempt), 
                                                     mask = BitMask32.bit(31),
                                                     penetration = .001) 
        
        if (result.hasHit()):
            intermediatePosition = self.position + speedVec * result.getHitFraction()
            remainingMovement = newPositionAttempt - intermediatePosition
            colisionNormal = result.getHitNormal()
            remainingMovementTangentComponent = remainingMovement - colisionNormal * remainingMovement.dot(colisionNormal)
            self.position = intermediatePosition
            self.tryToMoveXY2(remainingMovementTangentComponent)
        
        else:
            self.position = newPositionAttempt
        
    def tryToMoveXY2(self, speedVec):
        newPositionAttempt = self.position + speedVec      
        result = self.mainRef.world.sweepTestClosest(self.charBodySphereShapeMinor, 
                                                     TransformState.makePos(self.position), 
                                                     TransformState.makePos(newPositionAttempt), 
                                                     mask = BitMask32.bit(31),
                                                     penetration = .001)
        
        if (result.hasHit()):
            self.position = self.position + speedVec * result.getHitFraction()
        else:
            self.position = newPositionAttempt
        
    def tryToMoveZ(self, speedVec):
        self.fallingSpeed.addZ( self.accelerationStep * globalClock.getDt() ) 
        feetPosAttempt = self.position + Vec3(0,0,-1) * self.bodyHeight + self.fallingSpeed
        result = self.mainRef.world.rayTestClosest(self.position, feetPosAttempt + Vec3(0,0,-1), mask = BitMask32.bit(31) ) # "+Vec3(0,0,-1)" is intended to avoid problems at the borders
        self.stepNormal = result.getHitNormal()
        
        if (result.hasHit() and (feetPosAttempt.getZ()) < result.getHitPos().getZ()): # result.getHitPos().getZ() = floorHeight
            self.position = result.getHitPos() + Vec3(0,0,1) * self.bodyHeight
            self.fallingSpeed = Vec3(0,0,0)
        
        else:  
            self.position = self.position + self.fallingSpeed
        
        
    def destroy(self):
        "Destructor"
        # Remove bullet node
        self.mainRef.world.removeRigidBody(self.collisionNode)
        self.charBodyNP.removeNode()
        pass

        
        
        