from pandac.PandaModules import *
from direct.showbase.ShowBase import ShowBase
from panda3d.bullet import BulletWorld
from panda3d.bullet import BulletPlaneShape
from panda3d.bullet import BulletRigidBodyNode

import sys

from CameraHandler import *
from PlayerHUD import *    


class Main(ShowBase):
    def __init__(self):
        
        ShowBase.__init__(self)

        # camera
        self.camera.setPos(10,0,25)
        self.cameraHandler = CameraHandler(self)
        self.cameraHandler.registerFPSCameraInput()
        
        # disabling Panda's defauld cameraHandler
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
        # here there is the handler to use this time to manage collisions.
        collisionHandler = CollisionHandlerEvent()
        # initializing Bullet physics
        world = BulletWorld()
        world.setGravity(Vec3(0, 0, -9.81))
        
        # plane - flat infinite plane surface
        shape = BulletPlaneShape(Vec3(0, 0, 1), 1)
        node = BulletRigidBodyNode('Ground')
        node.addShape(shape)
        np = render.attachNewNode(node)
        np.setPos(0, 0, -2)
        world.attachRigidBody(node)
        
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

        # loading room
        self.testRoom = loader.loadModel("../../models/sala_teste")
        self.testRoom.reparentTo(self.render)
        self.testRoom.setPos(0, 0, -27)
        self.testRoom.setScale(34, 34, 34)
        
#        self.testRoom.ls()
        
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
        
        # loading student_chair model
        self.studentChairNP=NodePath(PandaNode("phisicschair"))
        self.studentChairModel = loader.loadModel("../../models/student_chair")
        self.studentChairModel.reparentTo(self.studentChairNP)
        self.studentChairCollider = self.studentChairModel.attachNewNode(CollisionNode('student_chaircnode'))
        self.studentChairCollider.node().addSolid(CollisionSphere(8, -5, 6, 10))
        self.studentChairNP.setPos(-2, 25,5)
        self.studentChairNP.setHpr(10.0,13.0,5.0)
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
        
        # updating Bullet physics engine
        def update(task):
            dt = globalClock.getDt()
            world.doPhysics(dt)
            return task.cont
        taskMgr.add(update, 'update')
       
main = Main()
# Starting mainLoop
main.run()