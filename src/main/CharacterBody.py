from panda3d.bullet import *
from pandac.PandaModules import *

class CharacterBody(object):
    
    def __init__(self, mainReference, initialPosition, bodyRadius, bodyHeight):
        self.mainRef = mainReference
        self.position = initialPosition
        self.bodyRadius = bodyRadius
        self.bodyHeight = bodyHeight
        self.stepNormal = ZUp
        
        self.accelerationStep = -9,81 / 60.0
        
        self.nextPosition = self.position
        
    def move(self, speedVec):
        self.tryToMoveXY(speedVec)
        self.tryToMoveZ(speedVec)
        return self.position
        
    def tryToMoveXY(self, speedVec):
        newPositionAttempt = self.position + speedVec     
        result = self.mainRef.world.sweepTestClosest(BulletSphereShape(.4), TransformState.makePos(self.position), TransformState.makePos(newPositionAttempt)) 
        
        if (result.hasHit()):
#            print "bateu!"
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
        result = self.mainRef.world.sweepTestClosest(BulletSphereShape(.3), TransformState.makePos(self.position), TransformState.makePos(newPositionAttempt))
        
        if (result.hasHit()):
#            print "bateu!"
            print self.position
            print speedVec, "speedVec"
            print result.getHitFraction()
            print ""
            self.position = self.position + speedVec * result.getHitFraction()
        else:
            self.position = newPositionAttempt
        
    def tryToMoveZ(self, speedVec):
        feetPosAttempt = self.position + Vec3(0,0,-1) * self.bodyHeight + Vec3(0,0,-0.02) #TODO
        result = self.mainRef.world.rayTestClosest(self.position, feetPosAttempt + Vec3(0,0,-1) ) # "+Vec3(0,0,-1)" is intended to avoid problems at the borders
        self.stepNormal = result.getHitNormal()
        
        if (result.hasHit() and (feetPosAttempt.getZ()) < result.getHitPos().getZ()): # result.getHitPos().getZ() = floorHeight
            self.position = result.getHitPos() + Vec3(0,0,1) * self.bodyHeight
        
        else:  
            self.position = self.position + Vec3(0,0,-0.02)
        
        
        

        
        
        