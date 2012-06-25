from panda3d.bullet import *
from pandac.PandaModules import *

class CharacterBody(object):
    
    def __init__(self, mainReference, initialPosition, bodyRadius, bodyHeight):
        self.mainRef = mainReference
        self.position = Point3(initialPosition)
        self.bodyRadius = bodyRadius
        self.bodyHeight = bodyHeight
        self.stepNormal = ZUp
        
        self.accelerationStep = -9,81 / 60.0
        
        self.nextPosition = self.position
        
    def move(self, speedVec):
        self.position = self.tryToMoveXY(speedVec)
        self.position = self.tryToMoveZ(speedVec)
        self.mainRef.camera.setPos(self.position)
        
    def tryToMoveXY(self, speedVec):
        newPositionAttempt = self.position + speedVec     
        result = self.mainRef.world.sweepTestClosest(BulletSphereShape(.4), TransformState.makePos(self.position), TransformState.makePos(newPositionAttempt))
        
        
        if (result.hasHit()):
#            print "bateu!"
            intermediatePosition = self.position + speedVec * result.getHitFraction()
            remainingMovement = newPositionAttempt - intermediatePosition
            colisionNormal = result.getHitNormal()
#            print colisionNormal.length()
            remainingMovementN = colisionNormal * remainingMovement.dot(colisionNormal)
            return intermediatePosition + (remainingMovement - remainingMovementN)
        
        else:
            return newPositionAttempt
        
    def tryToMoveXY2(self, direction, speedVec):
        newPositionAttempt = self.position + speedVec
        
        result = self.mainRef.world.sweepTestClosest(BulletSphereShape(.4), TransformState.makePos(self.position), TransformState.makePos(newPositionAttempt))
        
        
        if (result.hasHit()):
#            print "bateu!"
            intermediatePosition = self.position + speedVec * result.getHitFraction()
        
    def tryToMoveZ(self, speedVec):
        feetPosAttempt = self.position + Vec3(0,0,-1) * self.bodyHeight + Vec3(0,0,-.02)
        result = self.mainRef.world.rayTestClosest(self.position, feetPosAttempt + Vec3(0,0,-1) ) # "+Vec3(0,0,-1)" is intended to avoid problems at the borders
#        self.stepNormal = result.getHitNormal()
        
        if (result.hasHit() and (feetPosAttempt.getZ()) < result.getHitPos().getZ()): # result.getHitPos().getZ() = floorHeight
            return result.getHitPos() + Vec3(0,0,1) * self.bodyHeight
        
        else:  
            return self.position + Vec3(0,0,-.02)
        
        
        

        
        
        