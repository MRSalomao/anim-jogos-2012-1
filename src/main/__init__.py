from pandac.PandaModules import *
from direct.showbase.ShowBase import ShowBase
import sys

from CameraHandler import *       
from InputHandler import *    


class Main(ShowBase):
    def __init__(self):
        
        ShowBase.__init__(self)

        self.camera.setPos(10,0,25)
        
        self.cameraHandler = CameraHandler(self)
        
        self.inputHandler = InputHandler(self)
        self.inputHandler.setupFPSCameraInput()
        
        # Disabling Panda's defauld cameraHandler
        self.disableMouse()
        
        # fullscreen and hidden cursor
        wp = WindowProperties() 
#        wp.setFullscreen(True) 
        wp.setCursorHidden(True) 
        self.win.requestProperties(wp)
        
        # esc kills our game
        self.accept("escape",sys.exit)

        #** Collision system ignition - even if we're going to interact with the physics routines, the usual traverser is always in charge to drive collisions
        self.cTrav=CollisionTraverser()
        # look here: we enable the particle system - this is the evidence of what I was saying above, because the panda physics engine is conceived mainly to manage particles.
        self.enableParticles()
        # here there is the handler to use this time to manage collisions.
        collisionHandler = PhysicsCollisionHandler()
        
        #** This is the first time we see this collider: it is used mainly to define a flat infinite plane surface
        cp = CollisionPlane(Plane(Vec3(0, 0, 1), Point3(0, 0, 0)))
        planeNP = self.render.attachNewNode(CollisionNode('planecnode'))
        planeNP.node().addSolid(cp)
        planeNP.show()
        
        #** This is how to define the gravity force to make our stuff fall down: first off we define a ForceNode and attach to the render, so that everything below will be affected by this force
        globalforcesFN=ForceNode('world-forces')
        globalforcesFNP=self.render.attachNewNode(globalforcesFN)
        # then we set a linear force that will act in Z axis-drag-down-force of 9.81 units per second.
        globalforcesGravity=LinearVectorForce(0,0,-9.81)
        globalforcesFN.addForce(globalforcesGravity)
        # and then we assign this force to the physics manager. By the way, we never defined that manager, but it was made automatically when we called base.enableParticles()
        self.physicsMgr.addLinearForce(globalforcesGravity)
        
        # loading student_chair model 
        self.studentChairModel = loader.loadModel("../../models/student_chair")
        studentChairCollider = self.studentChairModel.attachNewNode(CollisionNode('student_chaircnode'))
        studentChairCollider.node().addSolid(CollisionSphere(0, 0, 0, 1))
        self.studentChairModel.reparentTo(render)
        self.studentChairModel.setPos(-2, 25,0)
        
        
main = Main()
# Starting mainLoop
main.run()