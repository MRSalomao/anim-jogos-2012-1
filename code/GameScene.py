'''
Created on 24/03/2012

'''
from pandac.PandaModules import *
from direct.showbase.DirectObject import DirectObject

import direct.directbase.DirectStart

class FirstPersonCamera(DirectObject):
    def __init__(self):
        # the below call only disables default mouse camera controls
        base.disableMouse()
        # disable mouse cursor
        props = WindowProperties()
        props.setCursorHidden(True) 
        base.win.requestProperties(props)
        #setup a position for our camera - this values are just for test purposes
        base.camera.setPos(0,-30,16)
        #initializers
        self.setupVars()
        self.setupInput()
        self.setupTasks()
        
    def setupVars(self):
        #speeds
        self.cameraSpeedRot = 0.05
        self.cameraSpeedMov = 0.1
        #keyboard movement triggers
        self.moveTowards  = False
        self.moveBackwards = False
        self.moveLeft  = False
        self.moveRight = False
        self.orbit = None 
        # getting mouse position
        if base.mouseWatcherNode.hasMouse():
            x=base.mouseWatcherNode.getMouseX()
            y=base.mouseWatcherNode.getMouseY()
            #TODO: add mouse functionality
            
    def setupInput(self):
        self.accept("w", self.setMoveTowards, [True])  
        self.accept("w-up", self.setMoveTowards, [False]) 
        self.accept("s", self.setMoveBackwards, [True]) 
        self.accept("s-up", self.setMoveBackwards, [False]) 
        self.accept("a", self.setMoveLeft, [True]) 
        self.accept("a-up", self.setMoveLeft, [False])
        self.accept("d", self.setMoveRight, [True]) 
        self.accept("d-up", self.setMoveRight, [False])
        self.accept("mouse3", self.setOrbit, [True]) 
        self.accept("mouse3-up", self.setOrbit, [False])

    def setupTasks(self):
        # handles keyboard movement
        taskMgr.add(self.cameraMove, "Camera Move")
        taskMgr.add(self.cameraOrbit, "Camera Orbit")
               
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
    def cameraMove(self, task): 
        if(self.moveTowards == True): 
            base.camera.setPos(base.camera.getPos().getX(),base.camera.getPos().getY()+self.cameraSpeedMov, base.camera.getPos().getZ())
        if(self.moveBackwards == True): 
            base.camera.setPos(base.camera.getPos().getX(),base.camera.getPos().getY()-self.cameraSpeedMov, base.camera.getPos().getZ())
        if(self.moveLeft == True): 
            base.camera.setPos(base.camera.getPos().getX()-self.cameraSpeedMov,base.camera.getPos().getY(), base.camera.getPos().getZ())
        if(self.moveRight == True): 
            base.camera.setPos(base.camera.getPos().getX()+self.cameraSpeedMov,base.camera.getPos().getY(), base.camera.getPos().getZ())     
        return task.cont
    
    def setOrbit(self, orbit): 
      if(orbit == True): 
         props = base.win.getProperties() 
         winX = props.getXSize() 
         winY = props.getYSize() 
         if base.mouseWatcherNode.hasMouse(): 
            mX = base.mouseWatcherNode.getMouseX() 
            mY = base.mouseWatcherNode.getMouseY() 
            mPX = winX * ((mX+1)/2) 
            mPY = winY * ((-mY+1)/2) 
         self.orbit = [[mX, mY], [mPX, mPY]] 
      else: 
         self.orbit = None 
    
    def cameraOrbit(self, task): 
      if(self.orbit != None): 
         if base.mouseWatcherNode.hasMouse(): 
             
            mpos = base.mouseWatcherNode.getMouse() 
             
            base.win.movePointer(0, int(self.orbit[1][0]), int(self.orbit[1][1])) 
             
            deltaH = 90 * (mpos[0] - self.orbit[0][0]) 
            deltaP = 90 * (mpos[1] - self.orbit[0][1]) 
             
            limit = .5 
             
            if(-limit < deltaH and deltaH < limit): 
               deltaH = 0 
            elif(deltaH > 0): 
               deltaH - limit 
            elif(deltaH < 0): 
               deltaH + limit 
                
            if(-limit < deltaP and deltaP < limit): 
               deltaP = 0 
            elif(deltaP > 0): 
               deltaP - limit 
            elif(deltaP < 0): 
               deltaP + limit 

            newH = (base.camera.getH() + -deltaH) 
            newP = (base.camera.getP() + deltaP) 
            if(newP < -90): newP = -90 
            if(newP > 90): newP = 90 
          
            base.camera.setHpr(newH, newP, 0)             
          
      return task.cont 

class World(DirectObject):
    def __init__(self):
        # camera load
        camera = FirstPersonCamera()
        #** Collision system ignition - even if we're going to interact with the physics routines, the usual traverser is always in charge to drive collisions
        base.cTrav=CollisionTraverser()
        # look here: we enable the particle system - this is the evidence of what I was saying above, because the panda physics engine is conceived mainly to manage particles.
        base.enableParticles()
        # here there is the handler to use this time to manage collisions.
        collisionHandler = PhysicsCollisionHandler()
        
        #** This is the first time we see this collider: it is used mainly to define a flat infinite plane surface
        cp = CollisionPlane(Plane(Vec3(0, 0, 1), Point3(0, 0, 0)))
        planeNP = base.render.attachNewNode(CollisionNode('planecnode'))
        planeNP.node().addSolid(cp)
        planeNP.show()
        
        #** This is how to define the gravity force to make our stuff fall down: first off we define a ForceNode and attach to the render, so that everything below will be affected by this force
        globalforcesFN=ForceNode('world-forces')
        globalforcesFNP=base.render.attachNewNode(globalforcesFN)
        # then we set a linear force that will act in Z axis-drag-down-force of 9.81 units per second.
        globalforcesGravity=LinearVectorForce(0,0,-9.81)
        globalforcesFN.addForce(globalforcesGravity)
        # and then we assign this force to the physics manager. By the way, we never defined that manager, but it was made automatically when we called base.enableParticles()
        base.physicsMgr.addLinearForce(globalforcesGravity)
        
        # loading student_chair model 
        self.studentChairModel = loader.loadModel("../models/student_chair")
        studentChairCollider = self.studentChairModel.attachNewNode(CollisionNode('student_chaircnode'))
        studentChairCollider.node().addSolid(CollisionSphere(0, 0, 0, 1))
        self.studentChairModel.reparentTo(render)
        self.studentChairModel.setPos(-2, 25,0)
        

# now we may start the game
world = World();
run()