from pandac.PandaModules import *
from main import *

from math import *
import time 

class CameraHandler(object):

    def __init__(self, mainReference):
        self.mainRef = mainReference
        
        self.cameraTaskList = []

        # 'K' stands for constants
        self.cameraRotationSpeedH_K = 0.06
        self.cameraRotationSpeedP_K = 0.05
        self.cameraMovementSpeed_K = 0.6
        
        # Rate at which the camera rotation/movement fades away
        self.rotationDamping_K = 0.65 
        self.movementDamping_K = 0.8
        
        self.moveTowards  = False
        self.moveBackwards = False
        self.moveLeft  = False
        self.moveRight = False
        
        # Intended to avoid excessive processing of mouse/keyboard input
        self.cameraLastUpdateTime = time.time()
        self.shouldUptade = True
        self.deltaTime = 0.0
        
        self.lastMousePosition = Vec2(0.0, 0.0)
        self.currentMousePosition = Vec2(0.0, 0.0)
        self.deltaMousePosition = Vec2(0.0, 0.0)
        
        self.cameraH = 0.0
        self.cameraP = 0.0
        self.cameraSpeedH = 0.0
        self.cameraSpeedP = 0.0
        
        self.cameraMoveDirectionVec = Vec2(0.0, 0.0)
        self.cameraMoveSpeedVec = Vec2(0.0, 0.0)
        
        taskMgr.add(self.frameRateWatcher, "frameRateWatcher", priority=2)
        taskMgr.add(self.updateCamera, "updateCamera", priority=1)
        
    
    def registerFPSCameraInput(self):
        self.cameraTaskList.append( self.mainRef.accept("w", self.setMoveTowards, [True]) )
        self.cameraTaskList.append( self.mainRef.accept("w-up", self.setMoveTowards, [False]) )
        self.cameraTaskList.append( self.mainRef.accept("s", self.setMoveBackwards, [True]) )
        self.cameraTaskList.append( self.mainRef.accept("s-up", self.setMoveBackwards, [False]) )
        self.cameraTaskList.append( self.mainRef.accept("a", self.setMoveLeft, [True]) )
        self.cameraTaskList.append( self.mainRef.accept("a-up", self.setMoveLeft, [False]) )
        self.cameraTaskList.append( self.mainRef.accept("d", self.setMoveRight, [True]) )
        self.cameraTaskList.append( self.mainRef.accept("d-up", self.setMoveRight, [False]) )
        
        
    def unregisterFPSCameraInput(self):
        while( not(self.cameraTaskList.empty()) ):
            self.cameraTaskList.pop().remove()
        
                   
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
        if (time.time() - self.cameraLastUpdateTime > .015):
            self.deltaTime = time.time() - self.cameraLastUpdateTime
            self.cameraLastUpdateTime = time.time()
            self.shouldUptade = True
            
        return task.cont 
            
        
    def updateCamera(self, task): 
        if (self.shouldUptade):  
            if self.mainRef.mouseWatcherNode.hasMouse(): 
                
                #    -Handle the keyboard events-
                if(self.moveRight == True):
                    self.cameraMoveDirectionVec.addX( sin(self.cameraH / 180 * pi + pi/2) )
                    self.cameraMoveDirectionVec.addY(-cos(self.cameraH / 180 * pi + pi/2) )
                    
                if(self.moveLeft == True):
                    self.cameraMoveDirectionVec.addX(-sin(self.cameraH / 180 * pi + pi/2) )
                    self.cameraMoveDirectionVec.addY( cos(self.cameraH / 180 * pi + pi/2) )
                
                if(self.moveBackwards == True):
                    self.cameraMoveDirectionVec.addX(-cos(self.cameraH / 180 * pi + pi/2) )
                    self.cameraMoveDirectionVec.addY(-sin(self.cameraH / 180 * pi + pi/2) )
                    
                if(self.moveTowards == True): 
                    self.cameraMoveDirectionVec.addX( cos(self.cameraH / 180 * pi + pi/2) )
                    self.cameraMoveDirectionVec.addY( sin(self.cameraH / 180 * pi + pi/2) )
            
                self.cameraMoveDirectionVec.normalize()
                
                self.cameraMoveSpeedVec += self.cameraMoveDirectionVec * self.cameraMovementSpeed_K
                
                self.mainRef.camera.setX(self.mainRef.camera.getX() + self.cameraMoveSpeedVec.getX())
                self.mainRef.camera.setY(self.mainRef.camera.getY() + self.cameraMoveSpeedVec.getY())
                
                self.cameraMoveSpeedVec *= self.movementDamping_K
                
                self.cameraMoveDirectionVec.set(0.0, 0.0)
                
                
                
                #    -Handle the mouse events-
                props = self.mainRef.win.getProperties() 
                winSizeX = props.getXSize() 
                winSizeY = props.getYSize()
                
                self.currentMousePosition = self.mainRef.mouseWatcherNode.getMouse() 
                
                self.deltaMousePosition.setX( winSizeX/2 - ( self.currentMousePosition.getX() + 1) / 2 * winSizeX)   
                self.deltaMousePosition.setY( winSizeY/2 - (-self.currentMousePosition.getY() + 1) / 2 * winSizeY)
                  
                self.cameraSpeedH += self.deltaMousePosition.getX() * self.cameraRotationSpeedH_K
                self.cameraSpeedP += self.deltaMousePosition.getY() * self.cameraRotationSpeedP_K
                
                self.cameraH += self.cameraSpeedH
                self.cameraP += self.cameraSpeedP  
                
                self.cameraSpeedH *= self.rotationDamping_K
                self.cameraSpeedP *= self.rotationDamping_K       
                
#                print(self.cameraH, self.cameraP)
                 
                # Just preventing the camera's 'R' from making it point to top or bottom
                if(self.cameraP > 89.9): 
                    self.cameraP = 89.9 
                if(self.cameraP < -89.9): 
                    self.cameraP = -89.9 
                     
                self.mainRef.camera.setHpr(self.cameraH, self.cameraP, 0)
        
                # This should prevent mouse from going outside of the window
                self.mainRef.win.movePointer(0, winSizeX/2, winSizeY/2)
        
        self.shouldUptade = False
        
        return task.cont 
