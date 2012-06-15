from pandac.PandaModules import *
from direct.filter.CommonFilters import CommonFilters
from direct.showbase.ShowBase import ShowBase
from panda3d.bullet import BulletWorld
from panda3d.bullet import BulletRigidBodyNode
from panda3d.bullet import BulletConvexHullShape
from panda3d.bullet import BulletDebugNode
from pathfind import *


import sys
from PlayerHUD import *
from Player import *
from EnemyManager import *
from Map import *   


class Main(ShowBase):
    def __init__(self):
        
        ShowBase.__init__(self)

        # disabling Panda's default cameraHandler
        self.disableMouse()
                
        # fullscreen and hidden cursor
        wp = WindowProperties() 
#        wp.setFullscreen(True) 
        wp.setCursorHidden(True) 
        self.win.requestProperties(wp)
        
        # esc kills our game
        self.accept("escape",sys.exit)
        
        # activating fps
        base.setFrameRateMeter(True)

        # Bullet debug purposes
        debugNode = BulletDebugNode('Debug')
        debugNode.showWireframe(True)
        debugNode.showConstraints(True)
        debugNode.showBoundingBoxes(False)
        debugNode.showNormals(False)
        debugNP = render.attachNewNode(debugNode)

        
        # initializing Bullet physics
        self.world = BulletWorld()
        self.world.setGravity(Vec3(0, 0, -9.81))
        self.world.setDebugNode(debugNP.node())

        # on/off debug mode
        def toggleDebug():
            if debugNP.isHidden():
                debugNP.show()
            else:
                debugNP.hide()
        
        self.accept('f1', toggleDebug)

######### Old pursue code        
        #Creating AI World
#        self.AIworld = PathWorld(10,10,10)
#########
        
        # loading student_chair model
        self.studentChairModel = loader.loadModel("../../models/student_chair")
        self.studentChairGeomNodes = self.studentChairModel.findAllMatches('**/+GeomNode')
        self.studentChairGeomNode = self.studentChairGeomNodes.getPath(0).node()
        self.studentChairGeom = self.studentChairGeomNode.getGeom(0)
        self.studentChairBulletShape = BulletConvexHullShape()
        self.studentChairBulletShape.addGeom(self.studentChairGeom)
        self.bulletChairNode = BulletRigidBodyNode('studentchair')
        self.bulletChairNode.setMass(2.0)
        self.bulletChairNode.addShape(self.studentChairBulletShape)
        np = render.attachNewNode(self.bulletChairNode)
        np.setPos(0,100,-23.10)
        self.world.attachRigidBody(self.bulletChairNode)
        self.studentChairModel.flattenLight()
        self.studentChairModel.reparentTo(np)
        
        # initializing player
        self.player = Player(self)       
        
        # initializing map
        self.map = Map(self)
        
        # initializing enemy manager
        self.enemyManager = EnemyManager(self)
        
        # initializing HUD
        self.playerHUD = PlayerHUD(self)
        
        # updating Bullet physics engine
        def update(task):
            dt = globalClock.getDt()
            self.world.doPhysics(dt)
            return task.cont
        taskMgr.add(update, 'update')

######### Old pursue code      
        #to update the AIWorld    
#        def AIUpdate(task):
#            self.AIworld.update()            
#            return Task.cont
        #AI World update        
#        taskMgr.add(AIUpdate,"AIUpdate")
#########

main = Main()
# Starting mainLoop
main.run()