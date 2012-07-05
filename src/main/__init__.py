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
                
        # fullscreen and hi dden cursor
        wp = WindowProperties() 
#        wp.setFullscreen(True) 
        wp.setCursorHidden(True) 
        self.win.requestProperties(wp)
        
        # esc kills our game
        self.accept("escape",sys.exit)
        
        # activating fps
        base.setFrameRateMeter(True)

        # Enable particles
        base.enableParticles()

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
                
        # activate bullet contact notification
        loadPrcFileData('', 'bullet-enable-contact-events true')
        
        self.accept('f1', toggleDebug)

        # initializing player
        self.player = Player(self)
        # allow player collision contact handling
        self.accept('bullet-contact-added', self.player.onContactAdded)      
        
        # initializing map
        self.map = Map(self)
        
        # initializing enemy manager
        self.enemyManager = EnemyManager(self)
        
        # initializing HUD
        self.playerHUD = PlayerHUD(self)
        
        # updating Bullet physics engine
        def update(task):
            dt = globalClock.getDt()
            self.world.doPhysics(dt, 4, 1./120.)
            return task.cont
        taskMgr.add(update, 'update')

main = Main()
# Starting mainLoop
main.run()