from pandac.PandaModules import *
from direct.showbase.ShowBase import ShowBase
from panda3d.ode import OdeWorld

import sys

from CameraHandler import *
from PlayerHUD import *    


class Main(ShowBase):
    def __init__(self):
        
        ShowBase.__init__(self)
        
        myWorld = OdeWorld()
        myWorld.setGravity(0, 0, -9.81)

        self.camera.setPos(10,0,25)
        
        self.cameraHandler = CameraHandler(self)
        self.cameraHandler.registerFPSCameraInput()
        
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
        collisionHandler = CollisionHandlerEvent()
        # physical collisions
        physicsHandler = PhysicsCollisionHandler()
        
        #** This is how to define the gravity force to make our stuff fall down: first off we define a ForceNode and attach to the render, so that everything below will be affected by this force
        globalforcesFN=ForceNode('world-forces')
        globalforcesFNP=self.render.attachNewNode(globalforcesFN)
        # then we set a linear force that will act in Z axis-drag-down-force of 9.81 units per second.
        globalforcesGravity=LinearVectorForce(0,0,-9.81)
        globalforcesFN.addForce(globalforcesGravity)
        # and then we assign this force to the physics manager. By the way, we never defined that manager, but it was made automatically when we called base.enableParticles()
        self.physicsMgr.addLinearForce(globalforcesGravity)
        
        #** This is the first time we see this collider: it is used mainly to define a flat infinite plane surface
        cp = CollisionPlane(Plane(Vec3(0, 0, 1), Point3(0, 0, 0)))
        planeNP = self.render.attachNewNode(CollisionNode('planecnode'))
        planeNP.node().addSolid(cp)
        planeNP.show()
        
        # adding collision node to our crosshair. Based on camera.
        self.pickerNode=CollisionNode('crosshairraycnode')
        self.crosshairNP=base.camera.attachNewNode(self.pickerNode)
        self.crosshairRay=CollisionRay(Point3(0,0,0),Vec3(0,1,0))
        self.pickerNode.addSolid(self.crosshairRay)
        self.pickerNode.setIntoCollideMask(BitMask32.allOff())
        base.cTrav.addCollider(self.crosshairNP, collisionHandler)
        
        # fog experiment
        myFog = Fog("Mist")
        myFog.setColor(0.6, 0.6, 0.6)
        myFog.setExpDensity(0.0007)
        render.setFog(myFog)

        # loading student_chair model
        # first off we gotta define the topmost node that should be a PandaNode wrapped into a nodepath - this is mandatory cos if we try to directly use the  Actornode defined below, we'll face inexpected behavior manipulating the object.
        self.studentChairNP=NodePath(PandaNode("phisicschair"))
        # we then need an ActorNode - this is required when playing with physics cos it got an interface suitable for this task while the usual nodepath ain't. Then we'll stick it to the main nodepath we'll put into the scene render node, wrapped into a nodepath of course.
        self.studentChairAN=ActorNode("chairactnode")
        self.studentChairANP=self.studentChairNP.attachNewNode(self.studentChairAN)
        
        self.testRoom = loader.loadModel("../../models/sala_teste")
        self.testRoom.reparentTo(self.render)
        self.testRoom.setPos(0, 0, -27)
        self.testRoom.setScale(34, 34, 34)
        
        self.testRoom.ls()
        
        self.tex = loader.loadTexture("../../models/floorlm.png")
        self.tsf = TextureStage('ts')
        self.tsf.setMode(TextureStage.MModulate)
        self.tsf.setTexcoordName("ul")      
        self.floor = self.testRoom.getChild(0).getChild(0)
        self.floor.setTexture(self.tsf, self.tex)
        
        self.tex = loader.loadTexture("../../models/floorlm.png")
        self.tsf = TextureStage('ts')
        self.tsf.setMode(TextureStage.MModulate)
        self.tsf.setTexcoordName("ul")      
        self.floor = self.testRoom.getChild(0).getChild(3)
        self.floor.setTexture(self.tsf, self.tex)
        
        self.tex2 = loader.loadTexture("../../models/wall2lm.png")
        self.tsw1 = TextureStage('ts1')
        self.tsw1.setMode(TextureStage.MModulate)
        self.tsw1.setTexcoordName("ul")      
        self.wall1 = self.testRoom.getChild(0).getChild(4)
        self.wall1.setTexture(self.tsw1, self.tex2)
        
        self.tex3 = loader.loadTexture("../../models/wall1lm.jpg")
        self.tsf1 = TextureStage('ts2')
        self.tsf1.setMode(TextureStage.MModulate)
        self.tsf1.setTexcoordName("ul")      
        self.floor = self.testRoom.getChild(0).getChild(2)
        self.floor.setTexture(self.tsf1, self.tex3)
        
        self.tex4 = loader.loadTexture("../../models/floor2lm.png")
        self.tsf2 = TextureStage('ts3')
        self.tsf2.setMode(TextureStage.MModulate)
        self.tsf2.setTexcoordName("ul")      
        self.floor = self.testRoom.getChild(0).getChild(1)
        self.floor.setTexture(self.tsf2, self.tex4)
        
        
        self.studentChairModel = loader.loadModel("../../models/student_chair")
        self.studentChairModel.reparentTo(self.studentChairANP)
        self.studentChairModel.setPos(-2, 25,50)
        self.studentChairModel.setHpr(10.0,13.0,5.0)
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
        # debug purposes - show collision solid
#        self.studentChairCollider.show()
        
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
        
        # initializing HUD
        self.playerHUD = PlayerHUD(self)
        
main = Main()
# Starting mainLoop
main.run()