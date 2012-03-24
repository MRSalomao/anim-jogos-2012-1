'''
Created on 24/03/2012

'''
from pandac.PandaModules import CollisionHandlerQueue, CollisionNode, CollisionSphere, CollisionTraverser
from direct.showbase.DirectObject import DirectObject

import direct.directbase.DirectStart

class World(DirectObject):
    def __init__(self):
        
        # loading student_chair model 
        self.studentChairModel = loader.loadModel("../models/student_chair")
        studentChairCollider = self.studentChairModel.attachNewNode(CollisionNode('student_chaircnode'))
        studentChairCollider.node().addSolid(CollisionSphere(0, 0, 0, 1))
        self.studentChairModel.reparentTo(render)
        self.studentChairModel.setPos(-2, 25,0)

# now we may start the game
world = World();
run()