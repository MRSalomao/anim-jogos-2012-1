from pandac.PandaModules import *

from math import *
import time 

class MovementHandler(object):
    
    degreeInRad = 3.1415 / 180

    def __init__(self, mainReference):
        self.mainRef = mainReference
        
        self.movementTaskList = []

        # 'K' stands for constants
        self.cameraRotationSpeedH_K = 0.04
        self.cameraRotationSpeedP_K = 0.03
        self.cameraMovementSpeed_K = 0.1
        
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
                self.playerMoveAccelerationVec *= self.cameraMovementSpeed_K
                
                self.playerMoveSpeedVec += self.playerMoveAccelerationVec
                self.playerMoveSpeedVec *= self.movementDamping_K

                self.playerMoveDirection = Vec3(self.playerMoveSpeedVec)
                self.playerMoveDirection.normalize()
                        
#                self.mainRef.camera.setPos( self.mainRef.player.playerBody.move(self.playerMoveSpeedVec) )
                self.mainRef.player.np.setPos( self.mainRef.player.playerBody.move(self.playerMoveSpeedVec) )
                self.checkIfChangedRegion()
                
                self.playerMoveAccelerationVec.set(0.0, 0.0, 0.0)
                
                #    -Handle the mouse events-
                props = self.mainRef.win.getProperties() 
                winSizeX = props.getXSize() 
                winSizeY = props.getYSize()
                
                self.currentMousePosition = self.mainRef.mouseWatcherNode.getMouse() 
                
                self.deltaMousePosition.setX( winSizeX/2 - ( self.currentMousePosition.getX() + 1) / 2 * winSizeX)   
                self.deltaMousePosition.setY( winSizeY/2 - (-self.currentMousePosition.getY() + 1) / 2 * winSizeY)
                  
                self.cameraSpeedH += self.deltaMousePosition.getX() * self.cameraRotationSpeedH_K
                self.cameraSpeedP += self.deltaMousePosition.getY() * self.cameraRotationSpeedP_K
                
                self.cameraP += self.cameraSpeedP
                self.cameraH += self.cameraSpeedH
                
                self.cameraSpeedH *= self.rotationDamping_K
                self.cameraSpeedP *= self.rotationDamping_K
                 
                # Just preventing the camera's 'P' from making it point to top or bottom
                if(self.cameraP > 89.9): 
                    self.cameraP = 89.9 
                if(self.cameraP < -89.9): 
                    self.cameraP = -89.9 
                
                self.mainRef.player.np.setHpr(self.cameraH, self.cameraP, 0)     
        
                # This should prevent mouse from going outside of the window
                self.mainRef.win.movePointer(0, winSizeX/2, winSizeY/2)
        
            self.shouldUptade = False
        
        return task.cont 
    
    
    def checkIfChangedRegion(self, lastRegion=0):
        i = 0
        for portal in self.mainRef.map.convexRegions[self.mainRef.player.currentRegion - 1].portalsList:
            
            if ( self.intersect( self.oldPosition, self.mainRef.camera.getPos(), portal.frontiers[0], portal.frontiers[1] )
                 and portal.connectedRegionsIDs[0] != lastRegion 
                 and portal.connectedRegionsIDs[1] != lastRegion ):
                lr = self.mainRef.player.currentRegion
                self.mainRef.player.currentRegion = self.mainRef.map.convexRegions[self.mainRef.player.currentRegion - 1].neighbourIDs[i]
                print "Player region changed: ", lr, ">", self.mainRef.player.currentRegion
                self.checkIfChangedRegion(lr)
                
            i += 1
        
        self.oldPosition = self.mainRef.camera.getPos()
              

    def ccw(self, A,B,C):
        return (C.getY()-A.getY())*(B.getX()-A.getX()) > (B.getY()-A.getY())*(C.getX()-A.getX())
    
    def intersect(self, A,B,C,D):
        return self.ccw(A,C,D) != self.ccw(B,C,D) and self.ccw(A,B,C) != self.ccw(A,B,D)

        
        
        
        
        
