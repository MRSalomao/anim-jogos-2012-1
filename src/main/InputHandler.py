from direct.showbase.ShowBase import ShowBase
from main import *

from CameraHandler import *       

class InputHandler(object):

    def __init__(self, mainReference):
        self.mainRef = mainReference
        
    def setupFPSCameraInput(self):
        self.mainRef.accept("w", self.mainRef.cameraHandler.setMoveTowards, [True])  
        self.mainRef.accept("w-up", self.mainRef.cameraHandler.setMoveTowards, [False]) 
        self.mainRef.accept("s", self.mainRef.cameraHandler.setMoveBackwards, [True]) 
        self.mainRef.accept("s-up", self.mainRef.cameraHandler.setMoveBackwards, [False]) 
        self.mainRef.accept("a", self.mainRef.cameraHandler.setMoveLeft, [True]) 
        self.mainRef.accept("a-up", self.mainRef.cameraHandler.setMoveLeft, [False])
        self.mainRef.accept("d", self.mainRef.cameraHandler.setMoveRight, [True]) 
        self.mainRef.accept("d-up", self.mainRef.cameraHandler.setMoveRight, [False])
        
