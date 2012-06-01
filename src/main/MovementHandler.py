from pandac.PandaModules import *

from math import *
import time 

class MovementHandler(object):

    def __init__(self, mainReference):
        self.mainRef = mainReference
        
        self.movementTaskList = []

        # 'K' stands for constants
        self.cameraRotationSpeedH_K = 3.30
        self.cameraRotationSpeedP_K = 0.03
        self.cameraMovementSpeed_K = 2.0
        
        # Rate at which the camera rotation/movement fades away
        self.rotationDamping_K = 0.65
        self.movementDamping_K = 0.65
        
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
        self.playerMoveSpeedVec = Vec3(0.0, 0.0, 0.0)
        
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
                    self.playerMoveAccelerationVec.setX( 1.0 )   
                if(self.moveLeft == True):
                    self.playerMoveAccelerationVec.setX( -1.0 )
                if(self.moveBackwards == True):
                    self.playerMoveAccelerationVec.setY( -1.0 )  
                if(self.moveTowards == True): 
                    self.playerMoveAccelerationVec.setY( 1.0 )
                    
                self.playerMoveAccelerationVec.normalize()
                self.playerMoveAccelerationVec *= self.cameraMovementSpeed_K
                
                self.playerMoveSpeedVec += self.playerMoveAccelerationVec
                self.playerMoveSpeedVec *= self.movementDamping_K
                        
                self.mainRef.player.playerNode.setLinearMovement(self.playerMoveSpeedVec, True)
                
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
                
                self.cameraSpeedH *= self.rotationDamping_K
                self.cameraSpeedP *= self.rotationDamping_K
                 
                # Just preventing the camera's 'P' from making it point to top or bottom
                if(self.cameraP > 89.9): 
                    self.cameraP = 89.9 
                if(self.cameraP < -89.9): 
                    self.cameraP = -89.9 
                     
                self.mainRef.camera.setHpr(0, self.cameraP, 0)
                
                # player character angulation
                self.mainRef.player.playerNode.setAngularMovement(self.cameraSpeedH)
        
                # This should prevent mouse from going outside of the window
                self.mainRef.win.movePointer(0, winSizeX/2, winSizeY/2)
        
        self.shouldUptade = False
        
        return task.cont 
