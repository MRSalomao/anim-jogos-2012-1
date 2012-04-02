'''
Created on 24/03/2012

'''
from pandac.PandaModules import *
from direct.showbase.DirectObject import DirectObject
from math import *

import sys
import direct.directbase.DirectStart

class FirstPersonCamera(DirectObject):
    
    currentTheta = 0.0
    
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
        self.cameraSpeedRot = 0.01
        self.cameraSpeedMov = 1
        #keyboard movement triggers
        self.moveTowards  = False
        self.moveBackwards = False
        self.moveLeft  = False
        self.moveRight = False
        self.orbit = None
        self.checkForMousePos = True
            
    def setupInput(self):
        self.accept("w", self.setMoveTowards, [True])  
        self.accept("w-up", self.setMoveTowards, [False]) 
        self.accept("s", self.setMoveBackwards, [True]) 
        self.accept("s-up", self.setMoveBackwards, [False]) 
        self.accept("a", self.setMoveLeft, [True]) 
        self.accept("a-up", self.setMoveLeft, [False])
        self.accept("d", self.setMoveRight, [True]) 
        self.accept("d-up", self.setMoveRight, [False])
        
        
    def setupTasks(self):
        # handles keyboard movement
        taskMgr.add(self.cameraMove, "Camera Move")
        taskMgr.add(self.captureMousePos, "Camera Orbit")
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
            base.camera.setPos(base.camera.getPos().getX() - self.cameraSpeedMov * sin(self.currentTheta / 180 * pi),
                               base.camera.getPos().getY() + self.cameraSpeedMov * cos(self.currentTheta / 180 * pi), 
                               base.camera.getPos().getZ() )  
            
        if(self.moveBackwards == True): 
            base.camera.setPos(base.camera.getPos().getX() + self.cameraSpeedMov * sin(self.currentTheta / 180 * pi),
                               base.camera.getPos().getY() - self.cameraSpeedMov * cos(self.currentTheta / 180 * pi), 
                               base.camera.getPos().getZ() )
            
        if(self.moveLeft == True): 
            base.camera.setPos(base.camera.getPos().getX() - self.cameraSpeedMov * cos(self.currentTheta / 180 * pi),
                               base.camera.getPos().getY() - self.cameraSpeedMov * sin(self.currentTheta / 180 * pi), 
                               base.camera.getPos().getZ() )
        if(self.moveRight == True): 
            base.camera.setPos(base.camera.getPos().getX() + self.cameraSpeedMov * cos(self.currentTheta / 180 * pi), 
                               base.camera.getPos().getY() + self.cameraSpeedMov * sin(self.currentTheta / 180 * pi), 
                               base.camera.getPos().getZ() )
            
               
        return task.cont
    
    def captureMousePos(self, task):   
        if (base.mouseWatcherNode.hasMouse() and self.checkForMousePos): 
            props = base.win.getProperties() 
            winX = props.getXSize() 
            winY = props.getYSize()
            mX = base.mouseWatcherNode.getMouseX() 
            mY = base.mouseWatcherNode.getMouseY()
            # our mouse X and Y range from -1 to 1, so we change this from 0 to 1 values and multiply by window size
            mPX = winX * ((mX+1)/2)
            mPY = winY * ((-mY+1)/2)
            self.orbit = [[mX, mY], [mPX, mPY]]
            self.checkForMousePos = False
        elif (base.mouseWatcherNode.hasMouse() == False): 
            self.checkForMousePos = True 
        return task.cont 
  
    def cameraOrbit(self, task):
        if(self.checkForMousePos == False): 
            if base.mouseWatcherNode.hasMouse(): 
               
                mpos = base.mouseWatcherNode.getMouse() 
              
                # first argument selects mouse; second and third sets the cursor position 
                base.win.movePointer(0, int(self.orbit[1][0]), int(self.orbit[1][1])) 
              
                # trying to catch some delta on our orientation 
                deltaH = 90 * (mpos[0] - self.orbit[0][0]) 
                deltaP = 90 * (mpos[1] - self.orbit[0][1]) 
               
                limit = .5 
              
                # fine tuning
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
            
                self.currentTheta = newH
                base.camera.setHpr(newH, newP, 0)
               
        return task.cont 

class World(DirectObject):
    def __init__(self):
        #fullscreen
#        wp = WindowProperties() 
#        wp.setFullscreen(True) 
#        base.win.requestProperties(wp)

        #esc kills our game
        self.accept("escape",sys.exit)
        
        # camera load
        camera = FirstPersonCamera()
        
        #** Collision system ignition - even if we're going to interact with the physics routines, the usual traverser is always in charge to drive collisions
        base.cTrav=CollisionTraverser()
        # look here: we enable the particle system - this is the evidence of what I was saying above, because the panda physics engine is conceived mainly to manage particles.
        base.enableParticles()
        # here there is the handler to use this time to manage collisions.
        collisionHandler = CollisionHandlerEvent()
        # physical collisions
        physicsHandler = PhysicsCollisionHandler()
        
        #** This is how to define the gravity force to make our stuff fall down: first off we define a ForceNode and attach to the render, so that everything below will be affected by this force
        globalforcesFN=ForceNode('world-forces')
        globalforcesFNP=base.render.attachNewNode(globalforcesFN)
        # then we set a linear force that will act in Z axis-drag-down-force of 9.81 units per second.
        globalforcesGravity=LinearVectorForce(0,0,-9.81)
        globalforcesFN.addForce(globalforcesGravity)
        # and then we assign this force to the physics manager. By the way, we never defined that manager, but it was made automatically when we called base.enableParticles()
        base.physicsMgr.addLinearForce(globalforcesGravity)

        #** This is the first time we see this collider: it is used mainly to define a flat infinite plane surface
        cp = CollisionPlane(Plane(Vec3(0, 0, 1), Point3(0, 0, 0)))
        planeNP = base.render.attachNewNode(CollisionNode('planecnode'))
        planeNP.node().addSolid(cp)
        # debug purposes
        planeNP.show()

        # adding collision node to our crosshair. Based on camera.
        self.pickerNode=CollisionNode('crosshairraycnode')
        self.crosshairNP=base.camera.attachNewNode(self.pickerNode)
        self.crosshairRay=CollisionRay(Point3(0,0,0),Vec3(0,1,0))
        self.pickerNode.addSolid(self.crosshairRay)
        base.cTrav.addCollider(self.crosshairNP, collisionHandler)

        # loading student_chair model
        # first off we gotta define the topmost node that should be a PandaNode wrapped into a nodepath - this is mandatory cos if we try to directly use the  Actornode defined below, we'll face inexpected behavior manipulating the object.
        self.studentChairNP=NodePath(PandaNode("phisicschair"))
        # we then need an ActorNode - this is required when playing with physics cos it got an interface suitable for this task while the usual nodepath ain't. Then we'll stick it to the main nodepath we'll put into the scene render node, wrapped into a nodepath of course.
        self.studentChairAN=ActorNode("chairactnode")
        self.studentChairANP=self.studentChairNP.attachNewNode(self.studentChairAN)
        self.studentChairModel = loader.loadModel("../models/student_chair")
        self.studentChairModel.reparentTo(self.studentChairANP)
        self.studentChairModel.setPos(-2, 25,50)
        self.studentChairCollider = self.studentChairModel.attachNewNode(CollisionNode('student_chaircnode'))
        self.studentChairCollider.node().addSolid(CollisionSphere(8, -5, 6, 10))
        # now it's a good time to dip our object into the physics environment (the Actornode btw)
        base.physicsMgr.attachPhysicalNode(self.studentChairAN)
        # then tell to the PhysicsCollisionHandler what are its collider and main nodepath to handle - this means that the ballANP nodepath will be phisically moved to react to all the physics forces we applied in the environment (the gravity force in the specific). Note that due we are using a particular collison handler (PhysicsCollisionHandler) we cannot pass a common nodepath as we did in all the previous steps but a nodepath-wrapped Actornode.
        physicsHandler.addCollider(self.studentChairCollider, self.studentChairANP)
        # and inform the main traverser as well
        base.cTrav.addCollider(self.studentChairCollider, physicsHandler)
        # now the physic ball is ready to exit off the dispenser - Note we reparent it to render by default
        self.studentChairNP.reparentTo(base.render)
        # debug purposes
        self.studentChairCollider.show()
        
        # collision handler methods
        def collideStudentChairIn(entry):
            print "colisao de entrada"
        def collideStudentChairOut(entry):
            print "colisao de saida"
        
        # adding a pattern - eases readability
        collisionHandler.addInPattern('%fn-into-%in')
        collisionHandler.addOutPattern('%fn-out-%in')

        # accepting student chair collision
        self.accept('crosshairraycnode-into-student_chaircnode', collideStudentChairIn)
        self.accept('crosshairraycnode-out-student_chaircnode', collideStudentChairOut)

        
# now we may start the game
world = World();
run()