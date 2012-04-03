from pandac.PandaModules import *
from main import *

import time
  
from InputHandler import *    

class CameraHandler(object):

    def __init__(self, mainReference):
        self.mainRef = mainReference

        self.cameraRotationSpeed = 0.01
        self.cameraMovementSpeed = 1
        
        self.moveTowards  = False
        self.moveBackwards = False
        self.moveLeft  = False
        self.moveRight = False
        
        # Intended to avoid excessive processing of mouse/keyboard input
        self.cameraUpdateTimer = time.time()
        
        self.lastMousePosition = [0.0, 0.0]#self.mainRef.mouseWatcherNode.getMouse()
        self.currentMousePosition = [0.0, 0.0]
        self.deltaMousePosition = [0.0, 0.0]
        
        self.cameraH = 0.0
        self.cameraR = 0.0
        
        taskMgr.add(self.moveCamera, "MoveCamera")
        taskMgr.add(self.aimCamera, "AimCamera")

               
    # this setters triggers keyboard movement of our camera    
    def setMoveTowards(self,value):
        self.moveTowards = value
    def setMoveBackwards(self,value):
        self.moveBackwards = value 
    def setMoveLeft(self,value):
        self.moveLeft = value   
    def setMoveRight(self,value):
        self.moveRight = value
    
    # the camera movement itself
    def moveCamera(self, task): 
        
        if(self.moveRight == True):
            self.mainRef.camera.setPos(self.mainRef.camera.getPos().getX() + self.cameraSpeedMov * sin(self.currentTheta / 180 * pi + pi/2),
                               self.mainRef.camera.getPos().getY() - self.cameraSpeedMov * cos(self.currentTheta / 180 * pi + pi/2), 
                               self.mainRef.camera.getPos().getZ() )
            
        if(self.moveLeft == True):
            self.mainRef.camera.setPos(self.mainRef.camera.getPos().getX() - self.cameraSpeedMov * sin(self.currentTheta / 180 * pi + pi/2),
                               self.mainRef.camera.getPos().getY() + self.cameraSpeedMov * cos(self.currentTheta / 180 * pi + pi/2), 
                               self.mainRef.camera.getPos().getZ() )
            
        if(self.moveBackwards == True):
            self.mainRef.camera.setPos(self.mainRef.camera.getPos().getX() - self.cameraSpeedMov * cos(self.currentTheta / 180 * pi + pi/2),
                               self.mainRef.camera.getPos().getY() - self.cameraSpeedMov * sin(self.currentTheta / 180 * pi + pi/2), 
                               self.mainRef.camera.getPos().getZ() )
            
        if(self.moveTowards == True): 
            self.mainRef.camera.setPos(self.mainRef.camera.getPos().getX() + self.cameraSpeedMov * cos(self.currentTheta / 180 * pi + pi/2), 
                               self.mainRef.camera.getPos().getY() + self.cameraSpeedMov * sin(self.currentTheta / 180 * pi + pi/2), 
                               self.mainRef.camera.getPos().getZ() )
            
        return task.cont


    def aimCamera(self, task):
#        self.aimCameraTimer = 
        
        if self.mainRef.mouseWatcherNode.hasMouse(): 
            
            props = self.mainRef.win.getProperties() 
            winX = props.getXSize() 
            winY = props.getYSize()
            
            self.currentMousePosition = self.mainRef.mouseWatcherNode.getMouse() 
            
            self.deltaMousePosition[0] = (self.lastMousePosition[0] - self.currentMousePosition[0]) #* winX
            self.deltaMousePosition[1] = (self.lastMousePosition[1] - self.currentMousePosition[1]) #* winY
              
            self.cameraH += self.deltaMousePosition[0]
            self.cameraR += self.deltaMousePosition[1]
            
            print(self.deltaMousePosition[0], self.deltaMousePosition[1])
            print(self.cameraH, self.cameraR)
             
            # Just preventing the camera's 'R' from making it point to top or bottom
            if(self.cameraR > 89.9): 
                self.cameraR = 89.9 
            if(self.cameraR < -89.9): 
                self.cameraR = -89.9 
                 
            self.mainRef.camera.setHpr(self.cameraH, self.cameraR, 0)
            
            # Update 'lastMousePosition' for the next call of this task
#            self.lastMousePosition = self.currentMousePosition
    
            # This should prevent mouse from going outside of the window
#            self.mainRef.win.movePointer(0, winX/2, winY/2) 
        
        return task.cont 
