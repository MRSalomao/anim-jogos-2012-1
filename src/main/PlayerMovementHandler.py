from pandac.PandaModules import *

from math import *
import time 

class MovementHandler(object):
    
    degreeInRad = 3.1415 / 180

    def __init__(self, mainReference):
        self.mainRef = mainReference
        
        self.movementTaskList = []
        
        self.playerIsJumping = False
        self.jumpSpeed = 0.0
        self.jumpAccel = 30.0
        
        self.walkSpeed = 0.12
        self.runSpeed = 0.20

        # 'K' stands for constants
        self.playerRotationSpeedH_K = 0.04
        self.playerRotationSpeedP_K = 0.03
        self.playerMovementSpeed_K = self.walkSpeed
        
        # Rate at which the camera rotation/movement fades away
        self.rotationDamping_K = 0.55
        self.movementDamping_K = 0.55
        
        self.moveTowards  = False
        self.moveBackwards = False
        self.moveLeft  = False
        self.moveRight = False
        
        # Intended to avoid excessive processing of mouse/keyboard input
        self.movementLastUpdateTime = time.time()
        self.shouldUptade = True
        self.deltaTime = 0.0
        
        self.lastMousePosition = Vec2(0.0, 0.0)
        self.currentMousePosition = Vec2(0.0, 0.0)
        self.deltaMousePosition = Vec2(0.0, 0.0)
        
        self.cameraH = 0.0
        self.cameraP = 0.0
        self.cameraSpeedH = 0.0
        self.cameraSpeedP = 0.0
        
        self.playerMoveAccelerationVec = Vec3(0.0, 0.0, 0.0)
        self.playerMoveDirection = Vec3(0.0, 0.0, 0.0)
        self.playerMoveSpeedVec = Vec3(0.0, 0.0, 0.0)
        
        self.oldPosition = self.mainRef.camera.getPos() 
        
        taskMgr.add(self.frameRateWatcher, "frameRateWatcher", priority=2)
        taskMgr.add(self.updateMovement, "updateMovement", priority=1)
        
    
    def registerFPSMovementInput(self):
        self.movementTaskList.append( self.mainRef.accept("w", self.setMoveTowards, [True]) )
        self.movementTaskList.append( self.mainRef.accept("w-up", self.setMoveTowards, [False]) )
        self.movementTaskList.append( self.mainRef.accept("s", self.setMoveBackwards, [True]) )
        self.movementTaskList.append( self.mainRef.accept("s-up", self.setMoveBackwards, [False]) )
        self.movementTaskList.append( self.mainRef.accept("a", self.setMoveLeft, [True]) )
        self.movementTaskList.append( self.mainRef.accept("a-up", self.setMoveLeft, [False]) )
        self.movementTaskList.append( self.mainRef.accept("d", self.setMoveRight, [True]) )
        self.movementTaskList.append( self.mainRef.accept("d-up", self.setMoveRight, [False]) )
        self.movementTaskList.append( self.mainRef.accept("shift", self.setSprint, [True]) )
        self.movementTaskList.append( self.mainRef.accept("shift-up", self.setSprint, [False]) ) 
        self.movementTaskList.append( self.mainRef.accept("space", self.jump, [True]) )
        
        
    def setSprint(self,value):
        if (value): 
            self.playerMovementSpeed_K = self.runSpeed
        else:
            self.playerMovementSpeed_K = self.walkSpeed
            
    def jump(self,value):  
        if (self.playerIsJumping == False):
            self.playerIsJumping = True
            self.jumpSpeed = 0.0
            taskMgr.add(self.jumpTask, "jump")
    
    def jumpTask(self, task):
        if (task.time < 0.7 ):
            self.jumpSpeed += self.jumpAccel * globalClock.getDt()
            self.mainRef.player.playerNP.setPos( self.mainRef.player.playerBody.move(Vec3(0,0,self.jumpSpeed)) )
            task.cont
            
        self.playerIsJumping = False
        task.done
            
        
    def unregisterFPSMovementInput(self):
        while( not(self.movementTaskList.empty()) ):
            self.movementTaskList.pop().remove()
         
    # this setters triggers keyboard movement of our camera    
    def setMoveTowards(self,value):
        self.moveTowards = value
    def setMoveBackwards(self,value):
        self.moveBackwards = value 
    def setMoveLeft(self,value):
        self.moveLeft = value   
    def setMoveRight(self,value):
        self.moveRight = value
        
    def frameRateWatcher(self, task):
        # Here we try to maintain something around 60 updates/s
        if (time.time() - self.movementLastUpdateTime > .015):
            self.deltaTime = time.time() - self.movementLastUpdateTime
            self.movementLastUpdateTime = time.time()
            self.shouldUptade = True
            
        return task.cont 
            
        
    def updateMovement(self, task): 
        if (self.shouldUptade):  
            if self.mainRef.mouseWatcherNode.hasMouse():
                
                #    -Handle the keyboard events-
                if(self.moveRight == True):
                    self.playerMoveAccelerationVec.addX(  cos(self.cameraH * MovementHandler.degreeInRad) )   
                    self.playerMoveAccelerationVec.addY(  sin(self.cameraH * MovementHandler.degreeInRad) )
                if(self.moveLeft == True):
                    self.playerMoveAccelerationVec.addX( -cos(self.cameraH * MovementHandler.degreeInRad) )
                    self.playerMoveAccelerationVec.addY(  -sin(self.cameraH * MovementHandler.degreeInRad) )
                if(self.moveBackwards == True):
                    self.playerMoveAccelerationVec.addX( sin(self.cameraH * MovementHandler.degreeInRad) )
                    self.playerMoveAccelerationVec.addY( -cos(self.cameraH * MovementHandler.degreeInRad) )  
                if(self.moveTowards == True): 
                    self.playerMoveAccelerationVec.addX(  -sin(self.cameraH * MovementHandler.degreeInRad) )
                    self.playerMoveAccelerationVec.addY(  cos(self.cameraH * MovementHandler.degreeInRad) )
      
                self.playerMoveAccelerationVec.normalize()
                self.playerMoveAccelerationVec *= self.playerMovementSpeed_K
                
                self.playerMoveSpeedVec += self.playerMoveAccelerationVec
                self.playerMoveSpeedVec *= self.movementDamping_K

                self.playerMoveDirection = Vec3(self.playerMoveSpeedVec)
                self.playerMoveDirection.normalize()
                        
                self.mainRef.player.playerNP.setPos( self.mainRef.player.playerBody.move(self.playerMoveSpeedVec) )
                self.checkIfChangedRegion()
                
                self.playerMoveAccelerationVec.set(0.0, 0.0, 0.0)
                
                #    -Handle the mouse events-
                props = self.mainRef.win.getProperties() 
                winSizeX = props.getXSize() 
                winSizeY = props.getYSize()
                
                self.currentMousePosition = self.mainRef.mouseWatcherNode.getMouse() 
                
                self.deltaMousePosition.setX( winSizeX/2 - ( self.currentMousePosition.getX() + 1) / 2 * winSizeX)   
                self.deltaMousePosition.setY( winSizeY/2 - (-self.currentMousePosition.getY() + 1) / 2 * winSizeY)
                  
                self.cameraSpeedH += self.deltaMousePosition.getX() * self.playerRotationSpeedH_K
                self.cameraSpeedP += self.deltaMousePosition.getY() * self.playerRotationSpeedP_K
                
                self.cameraP += self.cameraSpeedP
                self.cameraH += self.cameraSpeedH
                
                self.cameraSpeedH *= self.rotationDamping_K
                self.cameraSpeedP *= self.rotationDamping_K
                 
                # Just preventing the camera's 'P' from making it point to top or bottom
                if(self.cameraP > 89.9): 
                    self.cameraP = 89.9 
                if(self.cameraP < -89.9): 
                    self.cameraP = -89.9 
                
                self.mainRef.player.playerHeadNP.setHpr(self.cameraH, self.cameraP, 0)     
        
                # This should prevent mouse from going outside of the window
                self.mainRef.win.movePointer(0, winSizeX/2, winSizeY/2)
        
            self.shouldUptade = False
        
        return task.cont 
    
    
    def checkIfChangedRegion(self, lastRegion=0):

        for portalEntrance in self.mainRef.map.convexRegions[self.mainRef.player.currentRegionID].portalEntrancesList:
            
            if ( self.intersect( self.oldPosition, self.mainRef.player.playerNP.getPos(), 
                                 portalEntrance.portal.frontiers[0], portalEntrance.portal.frontiers[1] )
                                 and portalEntrance.portal.connectedRegionsIDs[0] != lastRegion 
                                 and portalEntrance.portal.connectedRegionsIDs[1] != lastRegion ):
                
                oldRegion = self.mainRef.player.currentRegionID
                self.mainRef.player.currentRegionID = portalEntrance.connectedRegionID
                
                # Debug
                print "Player region changed: ", oldRegion, ">", self.mainRef.player.currentRegionID
                
                # alert all enemys
                self.mainRef.enemyManager.disseminateTargetNewRegion()
                # check again
                self.checkIfChangedRegion(oldRegion)
        
        self.oldPosition = self.mainRef.player.playerNP.getPos()
              

    def ccw(self, A,B,C):
        return (C.getY()-A.getY())*(B.getX()-A.getX()) > (B.getY()-A.getY())*(C.getX()-A.getX())
    
    def intersect(self, A,B,C,D):
        return self.ccw(A,C,D) != self.ccw(B,C,D) and self.ccw(A,B,C) != self.ccw(A,B,D)

        
        
        
        
        
