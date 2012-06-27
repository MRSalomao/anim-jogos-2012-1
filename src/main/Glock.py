from pandac.PandaModules import *
from direct.actor.Actor import Actor
from direct.interval.IntervalGlobal import *

from Weapon import *

class Glock(Weapon):
    
    def __init__(self, mainReference):
        self.mainRef = mainReference
        super(Glock, self).__init__(mainReference)
        
        # load our glock model
        self.weaponModel = Actor("../../models/model_glock/glock")
        # ****SCALE****
        self.weaponModel.setScale(0.1)
        # ***POS***
        self.weaponModel.setPos(0.4,1.5,0.5)
        # ****HPR****
        self.weaponModel.setHpr(280,0,2)
        # attaching to render
        self.weaponModel.wrtReparentTo(self.mainRef)
        
    def shootAnim(self):
        super(Glock, self).shootAnim()
        
        seq=Sequence()
        seq.append( self.weaponModel.hprInterval(0.02,Point3(280,0,10), Point3(280,0,2) ) )
        seq.append( self.weaponModel.hprInterval(0.05,Point3(280,0, 2), Point3(280, 0, 10) ) )
        seq.start()
