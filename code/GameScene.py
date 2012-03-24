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
        # rotation angles. alpha refers to XY plane and beta refers to YZ plane.
        alphaAngle = 0.0
        betaAngle  = 0.0
        #speeds
        cameraSpeedRot = 0.05
        cameraSpeedMov = 0.2
        # getting mouse position
        if base.mouseWatcherNode.hasMouse():
            x=base.mouseWatcherNode.getMouseX()
            y=base.mouseWatcherNode.getMouseY()
        
        self.setupInput()
               
    def setupInput(self): 
        self.accept("w-repeat", self.setMoveTowards, [True]) 
        self.accept("w-up-repeat", self.setMoveTowards, [False]) 
        self.accept("s-repeat", self.setMoveBackwards, [True]) 
        self.accept("s-up-repeat", self.setMoveBackwards, [False]) 
        self.accept("a-repeat", self.setMoveLeft, [True]) 
        self.accept("a-up-repeat", self.setMoveLeft, [False])
        self.accept("d-repeat", self.setMoveRight, [True]) 
        self.accept("d-up-repeat", self.setMoveRight, [False])

    def setMoveTowards(self,value):
        if(value == True):
            base.camera.setPos(base.camera.getPos().getX(),base.camera.getPos().getY()+0.1, base.camera.getPos().getZ())     
    def setMoveBackwards(self,value): 
        base.camera.setPos(base.camera.getPos().getX(),base.camera.getPos().getY()-0.1, base.camera.getPos().getZ())
    def setMoveLeft(self,value):
        base.camera.setPos(base.camera.getPos().getX()-0.1,base.camera.getPos().getY(), base.camera.getPos().getZ())
    def setMoveRight(self,value): 
        base.camera.setPos(base.camera.getPos().getX()+0.1,base.camera.getPos().getY(), base.camera.getPos().getZ())

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